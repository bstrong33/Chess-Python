from piece import Piece

class Knight(Piece):
    def __init__(self, name, color, row, column, value):
        super().__init__(name, color, row, column, value)
    
    def calculate_possible_moves(self):
        self.possible_moves = []
        if self.row + 2 <= 8 and self.column + 1 <= 8:
            self.possible_moves.append([self.row + 2, self.column + 1])
        if self.row + 2 <= 8 and self.column - 1 >= 1:
            self.possible_moves.append([self.row + 2, self.column - 1])
        if self.row - 2 >= 1 and self.column + 1 <= 8:
            self.possible_moves.append([self.row - 2, self.column + 1])
        if self.row - 2 >= 1 and self.column - 1 >= 1:
            self.possible_moves.append([self.row - 2, self.column - 1])
        if self.row + 1 <= 8 and self.column + 2 <= 8:
            self.possible_moves.append([self.row + 1, self.column + 2])
        if self.row + 1 <= 8 and self.column - 2 >= 1:
            self.possible_moves.append([self.row + 1, self.column - 2])
        if self.row - 1 >= 1 and self.column + 2 <= 8:
            self.possible_moves.append([self.row - 1, self.column + 2])
        if self.row - 1 >= 1 and self.column - 2 >= 1:
            self.possible_moves.append([self.row - 1, self.column - 2])
        
        