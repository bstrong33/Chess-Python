from piece import Piece

class Rook(Piece):
    def __init__(self, name, color, row, column, value):
        super().__init__(name, color, row, column, value)
    
    def calculate_possible_moves(self):
        self.possible_moves = []
        for row in range(1, 9):
            if row != self.row:
                self.possible_moves.append([row, self.column])
        for column in range(1, 9):
            if column != self.column:
                self.possible_moves.append([self.row, column])