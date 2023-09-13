class Square:
    def __init__(self, color, row, column, piece=None):
        self.color = color
        self.row = row
        self.column = column
        self.piece = piece
        self.holding_piece = None

# holding_piece is used for check testing purposes if the square being tested already has a piece, it can save the original piece