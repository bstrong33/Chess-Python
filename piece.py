from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, name, color, row, column, value):
        self.name = name
        self.color = color
        self.row = row
        self.column = column
        self.value = value
        self.possible_moves = []
        self.has_moved = False
    
    @abstractmethod
    def calculate_possible_moves(self):
        pass