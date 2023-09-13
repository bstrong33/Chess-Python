from piece import Piece

class King(Piece):
    def __init__(self, name, color, row, column, value, in_check):
        super().__init__(name, color, row, column, value)
        self.in_check = in_check
        self.possible_squares_to_be_checked_from = []
        self.can_castle_kingside = False
        self.can_castle_queenside = False
    
    def calculate_possible_moves(self):
        self.possible_moves = []
        if self.row + 1 <= 8:
            self.possible_moves.append([self.row + 1, self.column])
            if self.column + 1 <= 8:
                self.possible_moves.append([self.row + 1, self.column + 1])
            if self.column - 1 >= 1:
                self.possible_moves.append([self.row + 1, self.column - 1])
        if self.row - 1 >= 1:
            self.possible_moves.append([self.row - 1, self.column])
            if self.column + 1 <= 8:
                self.possible_moves.append([self.row - 1, self.column + 1])
            if self.column - 1 >= 1:
                self.possible_moves.append([self.row - 1, self.column - 1])
        if self.column + 1 <= 8:
            self.possible_moves.append([self.row, self.column + 1])
        if self.column - 1 >= 1:
            self.possible_moves.append([self.row, self.column - 1])
    
    def calculate_possible_squares_to_be_checked_from(self):
        self.possible_squares_to_be_checked_from = []
        for row in range(1, 9):
            if row != self.row:
                self.possible_squares_to_be_checked_from.append([row, self.column])
        for column in range(1, 9):
            if column != self.column:
                self.possible_squares_to_be_checked_from.append([self.row, column])
        
        for spaces in range(1, 8):
            if self.row + spaces <= 8 and self.column + spaces <= 8:
                self.possible_squares_to_be_checked_from.append([self.row + spaces, self.column + spaces])
            if self.row - spaces >= 1 and self.column - spaces >= 1:
                self.possible_squares_to_be_checked_from.append([self.row - spaces, self.column - spaces])
            if self.row + spaces <= 8 and self.column - spaces >= 1:
                self.possible_squares_to_be_checked_from.append([self.row + spaces, self.column - spaces])
            if self.row - spaces >= 1 and self.column + spaces <= 8:
                self.possible_squares_to_be_checked_from.append([self.row - spaces, self.column + spaces])
        

