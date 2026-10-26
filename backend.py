from dataclasses import dataclass
from fontTools.pens.ttGlyphPen import TTGlyphPen, Glyph
from fontTools.fontBuilder import FontBuilder
from declarations import Bitmap, Bitmaps


class Font:
    def update_variables(
        self, bitmaps: Bitmaps, baseline_from_bottom=0, scale=100, unit_per_em=1000
    ):

        self.scale = scale

        # every glyph should be the same height!
        self.height = len(list(bitmaps.values())[0])

        # unit per em is canvas for a glyph. it most often should sum to 1000 or 2048
        # it is used for nice scaling so when user selects 6px font it scales to it
        self.unit_per_em: int = unit_per_em

        self.left_margin: int = scale
        self.right_margin: int = scale

        self.baseline = self.height - baseline_from_bottom
        # height - baseline from bottom is baseline from top

        self.ascent = self.baseline * scale
        self.descent = -1 * baseline_from_bottom * scale

        self.bitmaps: Bitmaps = bitmaps

    # for some fucking reason variables are copied and lists maps etc are references so pen is &pen
    def pixel_to_square(self, pen: TTGlyphPen, x: int, y: int) -> None:
        # 1.turning pixels into coordinates (see notes for more info)
        xmin = x * self.scale
        xmax = (x + 1) * self.scale
        ymin = (self.baseline - 1 - y) * self.scale
        ymax = (self.baseline - y) * self.scale

        # 2.building square based on coordinates above
        # moveTo = setting up paint lineTo = draws line from previous point to provided one
        pen.moveTo((xmin, ymin))
        pen.lineTo((xmax, ymin))
        pen.lineTo((xmax, ymax))
        pen.lineTo((xmin, ymax))
        pen.closePath()

    def bitmap_to_glyph(self, bitmap) -> Glyph:
        width: int = len(bitmap[0])

        pen: TTGlyphPen = TTGlyphPen(None)

        for y in range(self.height):
            for x in range(width):
                if bitmap[y][x]:
                    self.pixel_to_square(pen, x, y)

        return pen.glyph()

    def create_font(
        self, bitmaps: Bitmaps, name: str, output_path: str, baseline: int = 0
    ) -> None:  # none = void
        self.update_variables(bitmaps, baseline)
        # units per em is how many
        fb = FontBuilder(self.unit_per_em, isTTF=True)

        # .notdef is default glyph when selected one is missing. if we have only standard alphabet and want 'Ł' .notdef character will be used instead
        # glyphs contains models of characters ready for turning into font
        glyphs = {".notdef": TTGlyphPen(None).glyph()}

        # hmetrics are data about glyph
        # the first value (500 for notdef) means how far cursor should move after writing glyph
        # second is padding. if 0 it types character right on coursor
        hmetrics = {".notdef": (500, 0)}

        # cmap is dict of unicode codes mapped with characters which are keys for bitmaps
        cmap = {}

        for char_name, bitmap in self.bitmaps.items():
            glyphs[char_name] = self.bitmap_to_glyph(bitmap)

            width = len(bitmap[0])

            # scaled width with margins
            actual_width = width * self.scale + self.left_margin + self.right_margin

            cmap[ord(char_name)] = char_name

            hmetrics[char_name] = (actual_width, self.left_margin)

        # makes keys into glyph ids
        fb.setupGlyphOrder(list(glyphs.keys()))

        fb.setupCharacterMap(cmap)
        fb.setupGlyf(glyphs)
        fb.setupHorizontalMetrics(hmetrics)

        # baseline is y = 0 line
        # means how tall is the highes character form baseline and descent is how low is it from baseline
        fb.setupHorizontalHeader(ascent=self.ascent, descent=self.descent)

        # tbh i had problem with understanding this but from what i know it is used for windows fonts and web
        # u win descent is provided positive
        fb.setupOS2(
            sTypoAscender=self.ascent,
            usWinAscent=self.ascent,
            usWinDescent=(self.descent * -1),
        )

        fb.setupNameTable(
            {
                "familyName": name,
                "styleName": "Regular",  # it has to be regular otherwise it crashes
                "fullName": name,
                "psName": name.replace(" ", ""),
                "uniqueFontIdentifier": name,
            }
        )

        # this setups font
        fb.setupPost()

        fb.save(output_path)


if __name__ == "__main__":
    char_A = [
        [False, True, True, True, False],
        [True, False, False, False, True],
        [True, True, True, True, True],
        [True, False, False, False, True],
        [True, False, False, False, True],
    ]

    char_B = [
        [True, True, True, False, False],
        [True, False, False, True, False],
        [True, False, True, False, False],
        [True, False, False, True, False],
        [True, True, True, False, False],
    ]

    bitmaps = {"A": char_A, "B": char_B, "a": char_A, "b": char_B}

    font = Font()
    font.create_font(
        bitmaps,
        "font",
        "please_for_the_love_of_god_or_whoever_is_in_charge_of_the_universe_work.ttf",
    )
