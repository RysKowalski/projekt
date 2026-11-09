Bitmap = list[list[tuple[bool, int]]]  # (bool state, int amount)
Bitmaps = dict[str, Bitmap]


"""
dla przykładu
1 - True
0 - False

dla bitmapy:
1101
0010
1010
1111

powstaje obiekt:
[
    [(True, 2), (False, 1), (True, 1)],
    [(False, 2), (True, 1), (False, 1)],
    [(True, 1), (False, 1), (True, 1), (False, 1)],
    [(True, 4)],
]

w pierwszej liście znajdują się wszystkie wiersze
każdy wiersz jest listą
w tej liście znajdują się tuple/krotki z wartością True/False oznaczającą stan komurek,
oraz int oznaczającą ilość komórek o tej wartości z żędu

suma ilości komurek jest taka sama w każdym wierszu


obiekt:
[
    [(False, 3)],
    [(True, 2), (False, 1)],
    [(False, 1), (True, 1), (False, 1)]
]
reprezentuje:
000
110
010

"""
