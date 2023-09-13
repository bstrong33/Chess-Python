from piece import Piece

class Pawn(Piece):
    def __init__(self, name, color, row, column, value):
        super().__init__(name, color, row, column, value)
        self.just_moved_two = False
        self.can_au_passant = False
    
    def calculate_possible_moves(self):
        self.possible_moves = []
        if self.color == "white":
            if self.row + 1 <= 8:
                self.possible_moves.append([self.row + 1, self.column])
                if not self.has_moved:
                    self.possible_moves.append([self.row + 2, self.column])
                if self.column + 1 <= 8:
                    self.possible_moves.append([self.row + 1, self.column + 1])
                if self.column - 1 >= 1:
                    self.possible_moves.append([self.row + 1, self.column - 1])
        else:
            if self.row - 1 >= 1:
                self.possible_moves.append([self.row - 1, self.column])
                if not self.has_moved:
                    self.possible_moves.append([self.row - 2, self.column])
                if self.column + 1 <= 8:
                    self.possible_moves.append([self.row - 1, self.column + 1])
                if self.column - 1 >= 1:
                    self.possible_moves.append([self.row - 1, self.column - 1])