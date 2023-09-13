from piece import Piece

class Queen(Piece):
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
        
        for spaces in range(1, 8):
            if self.row + spaces <= 8 and self.column + spaces <= 8:
                self.possible_moves.append([self.row + spaces, self.column + spaces])
            if self.row - spaces >= 1 and self.column - spaces >= 1:
                self.possible_moves.append([self.row - spaces, self.column - spaces])
            if self.row + spaces <= 8 and self.column - spaces >= 1:
                self.possible_moves.append([self.row + spaces, self.column - spaces])
            if self.row - spaces >= 1 and self.column + spaces <= 8:
                self.possible_moves.append([self.row - spaces, self.column + spaces])