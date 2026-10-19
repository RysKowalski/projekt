from dataclasses import dataclass
from fontTools.pens.ttGlyphPen import TTGlyphPen
from declarations import Char, Bitmap

class Font:
    def __init__(self, bitmap: Bitmap, name: str, unit_per_em=1000, left_margin=100, baseline=150):
        self.name: str
        self.unit_per_em: int
        self.left_margin: int
        self.baseline: int


    # for some fucking reason variables are copied and lists maps etc are references so pen is &pen
    def pixel_to_square(self, pen: TTGlyphPen, x: int, y: int, scale: int, height: int):
        # 1.turning pixels into coordinates (see notes for more info)
        xmin = x * scale
        xmax = (x + 1) * scale
        ymin = (height - 1 - y) * scale
        ymax = (height - y) * scale

        # 2.building square based on coordinates above
        # moveTo = setting up paint lineTo = draws line from previous point to provided one
        pen.moveTo((xmin, ymin))
        pen.lineTo((xmax, ymin))
        pen.lineTo((xmax, ymax))
        pen.lineTo((xmin, ymax))
        pen.closePath()
    
    def bitmap_to_glyph(self, written_characters: Bitmap, scale=100):
        height: int = len(written_characters)
        width: int = len(bitmap[0])
        
        pen: TTGlyphPen = TTGlyphPen(None)

        for y in range(height):
            for x in range(width):
                if bitmap[y][x]:
                    self.pixel_to_square(pen, x, y, scale, height)

        return pen.glyph()


bitmap = [
    [False, False, True,  True,  False],
    [False, True,  False, False, True],
    [True,  True,  True,  True,  True],
    [True,  False, False, False, True],
    [True,  False, False, False, True],
]


