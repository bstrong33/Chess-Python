from square import Square
from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from rook import Rook
from pawn import Pawn


# class Board:
#     def __init__(self):
#         self.board = [
#             [Square('white', 8, 1, br1), Square('green', 8, 2, bn1), Square('white', 8, 3, bb1), Square('green', 8, 4, bq), Square('white', 8, 5, bk), Square('green', 8, 6, bb2), Square('white', 8, 7, bn2), Square('green', 8, 8, br2)],
#             [Square('green', 7, 1, bp1), Square("white", 7, 2, bp2), Square('green', 7, 3, bp3), Square("white", 7, 4, bp4), Square('green', 7, 5, bp5), Square("white", 7, 6, bp6), Square('green', 7, 7, bp7), Square("white", 7, 8, bp8)],
#             [Square('white', 6, 1), Square('green', 6, 2), Square('white', 6, 3), Square('green', 6, 4), Square('white', 6, 5), Square('green', 6, 6), Square('white', 6, 7), Square('green', 6, 8)],
#             [Square('green', 5, 1), Square('white', 5, 2), Square('green', 5, 3), Square('white', 5, 4), Square('green', 5, 5), Square('white', 5, 6), Square('green', 5, 7), Square('white', 5, 8)],
#             [Square('white', 4, 1), Square('green', 4, 2), Square('white', 4, 3), Square('green', 4, 4), Square('white', 4, 5), Square('green', 4, 6), Square('white', 4, 7), Square('green', 4, 8)],
#             [Square('green', 3, 1), Square('white', 3, 2), Square('green', 3, 3), Square('white', 3, 4), Square('green', 3, 5), Square('white', 3, 6), Square('green', 3, 7), Square('white', 3, 8)],
#             [Square('white', 2, 1, wp1), Square('green', 2, 2, wp2), Square('white', 2, 3, wp3), Square('green', 2, 4, wp4), Square('white', 2, 5, wp5), Square('green', 2, 6, wp6), Square('white', 2, 7, wp7), Square('green', 2, 8, wp8)],
#             [Square('green', 1, 1, wr1), Square("white", 1, 2, wn1), Square('green', 1, 3, wb1), Square("white", 1, 4, wq), Square('green', 1, 5, wk), Square("white", 1, 6, wb2), Square('green', 1, 7, wn2), Square("white", 1, 8, wr2)]
#         ]

class Board:
    def __init__(self):
        self.board = [
            [Square('green', 1, 1, wr1), Square("white", 1, 2, wn1), Square('green', 1, 3, wb1), Square("white", 1, 4, wq), Square('green', 1, 5, wk), Square("white", 1, 6, wb2), Square('green', 1, 7, wn2), Square("white", 1, 8, wr2)],
            [Square('white', 2, 1, wp1), Square('green', 2, 2, wp2), Square('white', 2, 3, wp3), Square('green', 2, 4, wp4), Square('white', 2, 5, wp5), Square('green', 2, 6, wp6), Square('white', 2, 7, wp7), Square('green', 2, 8, wp8)],
            [Square('green', 3, 1), Square('white', 3, 2), Square('green', 3, 3), Square('white', 3, 4), Square('green', 3, 5), Square('white', 3, 6), Square('green', 3, 7), Square('white', 3, 8)],
            [Square('white', 4, 1), Square('green', 4, 2), Square('white', 4, 3), Square('green', 4, 4), Square('white', 4, 5), Square('green', 4, 6), Square('white', 4, 7), Square('green', 4, 8)],
            [Square('green', 5, 1), Square('white', 5, 2), Square('green', 5, 3), Square('white', 5, 4), Square('green', 5, 5), Square('white', 5, 6), Square('green', 5, 7), Square('white', 5, 8)],
            [Square('white', 6, 1), Square('green', 6, 2), Square('white', 6, 3), Square('green', 6, 4), Square('white', 6, 5), Square('green', 6, 6), Square('white', 6, 7), Square('green', 6, 8)],
            [Square('green', 7, 1, bp1), Square("white", 7, 2, bp2), Square('green', 7, 3, bp3), Square("white", 7, 4, bp4), Square('green', 7, 5, bp5), Square("white", 7, 6, bp6), Square('green', 7, 7, bp7), Square("white", 7, 8, bp8)],
            [Square('white', 8, 1, br1), Square('green', 8, 2, bn1), Square('white', 8, 3, bb1), Square('green', 8, 4, bq), Square('white', 8, 5, bk), Square('green', 8, 6, bb2), Square('white', 8, 7, bn2), Square('green', 8, 8, br2)]
        ]

br1 = Rook("Rook", "black", 8, 1, 5)
bn1 = Knight("Knight", "black", 8, 2, 3)
bb1 = Bishop("Bishop", "black", 8, 3, 3)
bq = Queen("Queen", "black", 8, 4, 9)
bk = King("King", "black", 8, 5, 10, False)
bb2 = Bishop("Bishop", "black", 8, 6, 3)
bn2 = Knight("Knight", "black", 8, 7, 3)
br2 = Rook("Rook", "black", 8, 8, 5)

bp1 = Pawn("Pawn", "black", 7, 1, 1)
bp2 = Pawn("Pawn", "black", 7, 2, 1)
bp3 = Pawn("Pawn", "black", 7, 3, 1)
bp4 = Pawn("Pawn", "black", 7, 4, 1)
bp5 = Pawn("Pawn", "black", 7, 5, 1)
bp6 = Pawn("Pawn", "black", 7, 6, 1)
bp7 = Pawn("Pawn", "black", 7, 7, 1)
bp8 = Pawn("Pawn", "black", 7, 8, 1)

wp1 = Pawn("Pawn", "white", 2, 1, 1)
wp2 = Pawn("Pawn", "white", 2, 2, 1)
wp3 = Pawn("Pawn", "white", 2, 3, 1)
wp4 = Pawn("Pawn", "white", 2, 4, 1)
wp5 = Pawn("Pawn", "white", 2, 5, 1)
wp6 = Pawn("Pawn", "white", 2, 6, 1)
wp7 = Pawn("Pawn", "white", 2, 7, 1)
wp8 = Pawn("Pawn", "white", 2, 8, 1)

wr1 = Rook("Rook", "white", 1, 1, 5)
wn1 = Knight("Knight", "white", 1, 2, 3)
wb1 = Bishop("Bishop", "white", 1, 3, 3)
wq = Queen("Queen", "white", 1, 4, 9)
wk = King("King", "white", 1, 5, 10, False)
wb2 = Bishop("Bishop", "white", 1, 6, 3)
wn2 = Knight("Knight", "white", 1, 7, 3)
wr2 = Rook("Rook", "white", 1, 8, 5)
