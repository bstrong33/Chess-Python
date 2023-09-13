from piece import Piece

class Bishop(Piece):
    def __init__(self, name, color, row, column, value):
        super().__init__(name, color, row, column, value)
    
    def calculate_possible_moves(self):
        self.possible_moves = []
        for spaces in range(1, 8):
            if self.row + spaces <= 8 and self.column + spaces <= 8:
                self.possible_moves.append([self.row + spaces, self.column + spaces])
            if self.row - spaces >= 1 and self.column - spaces >= 1:
                self.possible_moves.append([self.row - spaces, self.column - spaces])
            if self.row + spaces <= 8 and self.column - spaces >= 1:
                self.possible_moves.append([self.row + spaces, self.column - spaces])
            if self.row - spaces >= 1 and self.column + spaces <= 8:
                self.possible_moves.append([self.row - spaces, self.column + spaces])
            