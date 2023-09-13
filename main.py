from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from board import Board
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight

class MainApp(App):
    def build(self):
        self.board = Board()
        # self.main_layout = BoxLayout(orientation="vertical")
        self.selected_piece = ""
        self.selected_row = 0
        self.selected_column = 0
        self.buttons = []
        self.index_of_selected_piece_button = None
        self.turn = "white"
        self.possible_moves = []
        self.checking_pieces = []
        self.display_text = "White's Turn"
        self.promotion_piece = ""
        self.promotion_row = 0
        self.promotion_column = 0

        self.main_layout = BoxLayout(
            orientation="horizontal",
            height = 600,
            width = 700,
        )

        self.board_layout = BoxLayout(
            orientation="vertical",
            height = 600,
            width = 600,
        )

        self.control_panel = BoxLayout(
            orientation="vertical",
            height = 600,
            width = 200,
            size_hint = (None, 1)
        )
        
        self.promotion_options = BoxLayout(
            orientation="vertical",
            height = 125,
            width = 200,
            size_hint = (1, None)
        )

        self.resign_black = Button(
            text = "Resign as Black",
            height = 25,
            width = 200,
            size_hint = (1, None)
        )
        self.resign_white = Button(
            text = "Resign as White",
            height = 25,
            width = 200,
            size_hint = (1, None)
        )

        self.display = Label(
            text = self.display_text
        )

        self.new_game = Button(
            text="Start New Game",
            height = 25,
            width = 100,
            size_hint = (1, None)
        )

        self.resign_white.bind(on_press=self.resign_with_white)
        self.resign_black.bind(on_press=self.resign_with_black)
        self.new_game.bind(on_press=self.start_new_game)

        self.control_panel.add_widget(self.resign_black)
        self.control_panel.add_widget(self.display)
        self.control_panel.add_widget(self.resign_white)

        self.main_layout.add_widget(self.control_panel)

        self.promotion_label = Label(
            text="Select Piece",
            height = 25,
            width = 100,
            size_hint = (1, None)
        )

        self.knight_button = Button(
            text = "Knight",
            height = 25,
            width = 100,
            size_hint = (1, None)
        )

        self.bishop_button = Button(
            text = "Bishop",
            height = 25,
            width = 100,
            size_hint = (1, None)
        )

        self.rook_button = Button(
            text = "Rook",
            height = 25,
            width = 100,
            size_hint = (1, None)
        )

        self.queen_button = Button(
            text = "Queen",
            height = 25,
            width = 100,
            size_hint = (1, None)
        )

        self.knight_button.bind(on_press=self.knight_promotion)
        self.bishop_button.bind(on_press=self.bishop_promotion)
        self.rook_button.bind(on_press=self.rook_promotion)
        self.queen_button.bind(on_press=self.queen_promotion)

        self.promotion_options.add_widget(self.promotion_label)
        self.promotion_options.add_widget(self.knight_button)
        self.promotion_options.add_widget(self.bishop_button)
        self.promotion_options.add_widget(self.rook_button)
        self.promotion_options.add_widget(self.queen_button)

        for row in reversed(self.board.board):
            h_layout = BoxLayout(
                height = 75,
                width = 600,
                size_hint = (1, 1),
                padding = 0,
                spacing = 0
            )

            for square in row:
                if square.piece:
                    name = square.piece.name
                    color = square.piece.color
                else:
                    name = ""
                button = Button(
                    text=name,
                    color=color,
                    height = 75,
                    width = 75,
                    background_color=square.color,
                    ids={0: square}
                )
                   
                self.buttons.append(button)
                button.bind(on_press=self.on_square_press)
                h_layout.add_widget(button)
            
            self.board_layout.add_widget(h_layout)
        
        self.main_layout.add_widget(self.board_layout)
        return self.main_layout

    def on_square_press(self, instance):
        board = self.board.board
        square = instance.ids[0]
        button_index = self.buttons.index(instance)
        if square.piece and square.piece.color == self.turn:
            # If selected square has a piece of the right color, updates state with this piece
            self.selected_piece = square.piece
            self.selected_row = square.piece.row
            self.selected_column = square.piece.column
            self.index_of_selected_piece_button = button_index
            self.selected_piece.calculate_possible_moves()
            
            if self.selected_piece.name == "Pawn":
                pawn_movement(self, board, self.selected_piece)
            if self.selected_piece.name == "Rook":
                rook_movement(self, board, self.selected_piece)
            if self.selected_piece.name == "Bishop":
                bishop_movement(self, board, self.selected_piece)
            if self.selected_piece.name == "Queen":
                rook_movement(self, board, self.selected_piece)
                bishop_movement(self, board, self.selected_piece)
            if self.selected_piece.name == "King":
                self.selected_piece.can_castle_kingside = False
                self.selected_piece.can_castle_queenside = False
                king_movement(self, board, self.selected_piece)
                check_castling(self, board, self.selected_piece)
            
            # reset all pawns to having not moved two squares if enemy didn't au passant
            for row in range(8):
                for col in range(8):
                    if board[row][col].piece and board[row][col].piece.name == "Pawn" and board[row][col].piece.color == self.turn:
                        board[row][col].piece.just_moved_two = False
        else:
            if self.selected_piece != "":
                for row in range(8):
                    for col in range(8):
                        if board[row][col].row == square.row and board[row][col].column == square.column and [square.row, square.column] in self.selected_piece.possible_moves:

                            king = ""
                            for row2 in range(8):
                                for col2 in range(8):
                                    if board[row2][col2].piece:
                                        if board[row2][col2].piece.name == "King" and board[row2][col2].piece.color == self.turn:
                                            king = board[row2][col2].piece

                            # Check if moving to this square will cause own king to be in check

                            board[row][col].holding_piece = board[row][col].piece
                            board[row][col].piece = self.selected_piece

                            board[self.selected_row - 1][self.selected_column - 1].holding_piece = board[self.selected_row - 1][self.selected_column - 1].piece

                            board[self.selected_row - 1][self.selected_column - 1].piece = None

                            king.in_check = False

                            # Specifically check if a king's move will cause it to still be in check
                            if self.selected_piece.name == "King" and not check_if_king_in_check(self, board, King("King", king.color, board[row][col].row, board[row][col].column, 10, False)):
                                # Update the new square with the selected piece
                                board[row][col].piece = self.selected_piece
                                instance.text = self.selected_piece.name
                                instance.color = self.selected_piece.color

                                # Update the selected piece with it's new row and column and has_moved property
                                board[row][col].piece.row = board[row][col].row
                                board[row][col].piece.column = board[row][col].column
                                board[row][col].piece.has_moved = True

                                # Update old square to no longer have a piece
                                board[self.selected_row - 1][self.selected_column - 1].piece = None
                                self.buttons[self.index_of_selected_piece_button].text = ""

                                # Resets selected piece to nothing
                                self.selected_piece = ""

                                # Changes turn color
                                if self.turn == "white":
                                    self.turn = "black"
                                    self.display_text = "Black's Turn"
                                    app.display.text = "Black's Turn"
                                else:
                                    self.turn = "white"
                                    self.display_text = "White's Turn"
                                    app.display.text = "White's Turn"

                                king = ""
                                for row3 in range(8):
                                    for col3 in range(8):
                                        if board[row3][col3].piece:
                                            if board[row3][col3].piece.name == "King" and board[row3][col3].piece.color == self.turn:
                                                king = board[row3][col3].piece
                                
                                # Check if move puts enemy king into check
                                if check_if_king_in_check(self, board, king):
                                    check_for_checkmate(self, board, king)
                                else:
                                    check_for_stalemate(self, board)

                            # Check if any other piece move will cause own king to be in check
                            elif check_if_king_in_check(self, board, king):
                                print("This causes the king to be in check")
                                board[row][col].piece = board[row][col].holding_piece
                                board[row][col].holding_piece = None

                                board[self.selected_row - 1][self.selected_column - 1].piece = board[self.selected_row - 1][self.selected_column - 1].holding_piece

                                board[self.selected_row - 1][self.selected_column - 1].holding_piece = None
                            
                            # Handles au passant movement and updates board
                            elif self.selected_piece.name == "Pawn" and self.selected_piece.can_au_passant and board[row][col].column != self.selected_piece.column:
                                print("au passant")
                                execute_au_passant(self, board, row, col, instance)

                                king = ""
                                for row6 in range(8):
                                    for col6 in range(8):
                                        if board[row6][col6].piece:
                                            if board[row6][col6].piece.name == "King" and board[row6][col6].piece.color == self.turn:
                                                king = board[row6][col6].piece
                                
                                # Check if move puts enemy king into check
                                if check_if_king_in_check(self, board, king):
                                    check_for_checkmate(self, board, king)
                                else:
                                    check_for_stalemate(self, board)
                            
                            # Handle Pawn Promotion
                            elif self.selected_piece.name == "Pawn" and (board[row][col].row == 1 or board[row][col].row == 8):
                                print("About to promote")
                                self.turn = ""
                                self.promotion_row = board[row][col].row
                                self.promotion_column = board[row][col].column
                                app.control_panel.add_widget(self.promotion_options)

                            # If selected piece move won't put own king in check, update the board with this move
                            else:
                                # If pawn moves foward two, set this attribute to True
                                if self.selected_piece.name == "Pawn" and (board[row][col].row - 2 == self.selected_piece.row or board[row][col].row + 2 == self.selected_piece.row):
                                    self.selected_piece.just_moved_two = True
                                    
                                # Update the new square with the selected piece
                                board[row][col].piece = self.selected_piece
                                instance.text = self.selected_piece.name
                                instance.color = self.selected_piece.color

                                # Update the selected piece with it's new row and column and has_moved property
                                board[row][col].piece.row = board[row][col].row
                                board[row][col].piece.column = board[row][col].column
                                board[row][col].piece.has_moved = True

                                # Update old square to no longer have a piece
                                board[self.selected_row - 1][self.selected_column - 1].piece = None
                                self.buttons[self.index_of_selected_piece_button].text = ""

                                # Resets selected piece to nothing
                                self.selected_piece = ""

                                # Changes turn color
                                if self.turn == "white":
                                    self.turn = "black"
                                    self.display_text = "Black's Turn"
                                    app.display.text = "Black's Turn"
                                else:
                                    self.turn = "white"
                                    self.display_text = "White's Turn"
                                    app.display.text = "White's Turn"

                                king = ""
                                for row4 in range(8):
                                    for col4 in range(8):
                                        if board[row4][col4].piece:
                                            if board[row4][col4].piece.name == "King" and board[row4][col4].piece.color == self.turn:
                                                king = board[row4][col4].piece
                                
                                # Check if move puts enemy king into check
                                if check_if_king_in_check(self, board, king):
                                    check_for_checkmate(self, board, king)
                                else:
                                    check_for_stalemate(self, board)

                        # Handles the movement and board updates for castling
                        elif board[row][col].row == square.row and board[row][col].column == square.column and self.selected_piece.name == "King" and not self.selected_piece.has_moved:
                            execute_castling_logic(self, board, row, col, instance)

                            king = ""
                            for row5 in range(8):
                                for col5 in range(8):
                                    if board[row5][col5].piece:
                                        if board[row5][col5].piece.name == "King" and board[row5][col5].piece.color == self.turn:
                                            king = board[row5][col5].piece
                            
                            # Check if move puts enemy king into check
                            if check_if_king_in_check(self, board, king):
                                check_for_checkmate(self, board, king)
                            else:
                                check_for_stalemate(self, board)
    
    def knight_promotion(self, instance):
        self.promotion_piece = "Knight"
        handle_promotion(self)
    
    def bishop_promotion(self, instance):
        self.promotion_piece = "Bishop"
        handle_promotion(self)
    
    def rook_promotion(self, instance):
        self.promotion_piece = "Rook"
        handle_promotion(self)
    
    def queen_promotion(self, instance):
        self.promotion_piece = "Queen"
        handle_promotion(self)
    
    def resign_with_white(self, instance):
        if self.turn != "":
            self.turn = ""
            self.display_text = "Black Wins!"
            app.display.text = "Black Wins!"
            app.control_panel.add_widget(self.new_game)

    def resign_with_black(self, instance):
        if self.turn != "":
            self.turn = ""
            self.display_text = "White Wins!"
            app.display.text = "White Wins!"
            app.control_panel.add_widget(self.new_game)
    
    def start_new_game(self, instance):
        print("About to start new game")
        nb = Board()
        board = self.board.board
        new_board = nb.board
        button_index = 0

        for row in range(8):
            for col in range(8):
                board[row][col].piece = None
        
        for row2 in reversed(range(8)):
            for col2 in range(8):
                board[row2][col2].piece = new_board[row2][col2].piece
                if board[row2][col2].piece:
                    board[row2][col2].piece.row = board[row2][col2].row
                    board[row2][col2].piece.column = board[row2][col2].column
                    board[row2][col2].piece.has_moved = False
                    board[row2][col2].piece.color = new_board[row2][col2].piece.color
                    self.buttons[button_index].text = board[row2][col2].piece.name
                    self.buttons[button_index].color = new_board[row2][col2].piece.color
                else:
                    self.buttons[button_index].text = ""
                button_index += 1

        self.display_text = "White's Turn"
        app.display.text = "White's Turn!"
        self.turn = "white"
        self.control_panel.remove_widget(self.new_game)

def handle_promotion(self):
    board = self.board.board

    # Give the promotion square the desired new piece
    for row in range(8):
        for col in range(8):
            if board[row][col].row == self.promotion_row and board[row][col].column == self.promotion_column:
                if self.promotion_piece == "Knight":
                    board[row][col].piece = Knight("Knight", self.selected_piece.color, self.promotion_row, self.promotion_column, 3)
                elif self.promotion_piece == "Bishop":
                    board[row][col].piece = Bishop("Bishop", self.selected_piece.color, self.promotion_row, self.promotion_column, 3)
                elif self.promotion_piece == "Rook":
                    board[row][col].piece = Rook("Rook", self.selected_piece.color, self.promotion_row, self.promotion_column, 5)
                elif self.promotion_piece == "Queen":
                    board[row][col].piece = Queen("Queen", self.selected_piece.color, self.promotion_row, self.promotion_column, 9)
            
            # Set the text and color at the promotion square
            if self.selected_piece.color == "white":
                self.buttons[self.promotion_column - 1].text = self.promotion_piece
                self.buttons[self.promotion_column - 1].color = self.selected_piece.color
            
            if self.selected_piece.color == "black":
                self.buttons[self.promotion_column + 55].text = self.promotion_piece
                self.buttons[self.promotion_column + 55].color = self.selected_piece.color
    
    # Update old pawn square to no longer have a piece
    board[self.selected_row - 1][self.selected_column - 1].piece = None
    self.buttons[self.index_of_selected_piece_button].text = ""
    
    # Changes turn color
    if self.selected_piece.color == "white":
        self.turn = "black"
        self.display_text = "Black's Turn"
        app.display.text = "Black's Turn"
    else:
        self.turn = "white"
        self.display_text = "White's Turn"
        app.display.text = "White's Turn"

    # Resets selected piece to nothing
    self.selected_piece = ""

    # Resets Promotional state
    self.promotion_piece = ""
    self.promotion_row = 0
    self.promtion_column = 0
    self.control_panel.remove_widget(self.promotion_options)

    # Check for checks after promotion
    king = ""
    for row2 in range(8):
        for col2 in range(8):
            if board[row2][col2].piece:
                if board[row2][col2].piece.name == "King" and board[row2][col2].piece.color == self.turn:
                    king = board[row2][col2].piece
    
    # Check if move puts enemy king into check
    if check_if_king_in_check(self, board, king):
        check_for_checkmate(self, board, king)
    else:
        check_for_stalemate(self, board)


def check_for_stalemate(self, board):
    for row in range(8):
        for col in range(8):
            if board[row][col].piece and board[row][col].piece.color == self.turn:
                board[row][col].piece.calculate_possible_moves()
                if board[row][col].piece.name == "Pawn":
                    pawn_movement(self, board, board[row][col].piece)
                if board[row][col].piece.name == "Bishop":
                    bishop_movement(self, board, board[row][col].piece)
                if board[row][col].piece.name == "Rook":
                    rook_movement(self, board, board[row][col].piece)
                if board[row][col].piece.name == "Queen":
                    rook_movement(self, board, board[row][col].piece)
                    bishop_movement(self, board, board[row][col].piece)
                if board[row][col].piece.name == "King":
                    king_movement(self, board, board[row][col].piece)
                if board[row][col].piece.possible_moves:
                    # print(board[row][col].piece.name, board[row][col].piece.possible_moves)
                    return False
                
    print("Stalemate")
    self.display_text = "Stalemate, it's a draw"
    app.display.text = "Stalemate, it's a draw"
    self.turn = ""
    app.control_panel.add_widget(self.new_game)
    return True
                

def execute_au_passant(self, board, row, col, instance):
    if self.selected_piece.color == "white" and board[row - 1][col].piece and board[row - 1][col].piece.name == "Pawn" and board[row - 1][col].piece.just_moved_two and board[row - 1][col].piece.color != self.selected_piece.color:
        # Update the new square with the selected piece
        board[row][col].piece = self.selected_piece
        instance.text = self.selected_piece.name
        instance.color = self.selected_piece.color

        #Update the enemy pawn square
        board[row - 1][col].piece = None
        if board[row][col].column < self.selected_piece.column:
            self.buttons[self.index_of_selected_piece_button - 1].text = ""
        else:
            self.buttons[self.index_of_selected_piece_button + 1].text = ""
        
        # Update the selected piece with it's new row and column and has_moved property
        board[row][col].piece.row = board[row][col].row
        board[row][col].piece.column = board[row][col].column
        board[row][col].piece.has_moved = True
        board[row][col].can_au_passant = False

        # Update old square to no longer have a piece
        board[self.selected_row - 1][self.selected_column - 1].piece = None
        self.buttons[self.index_of_selected_piece_button].text = ""

        # Resets selected piece to nothing
        self.selected_piece = ""

        # Changes turn color
        if self.turn == "white":
            self.turn = "black"
            self.display_text = "Black's Turn"
            app.display.text = "Black's Turn"
        else:
            self.turn = "white"
            self.display_text = "White's Turn"
            app.display.text = "White's Turn"

    elif self.selected_piece.color == "black" and board[row + 1][col].piece and board[row + 1][col].piece.name == "Pawn" and board[row + 1][col].piece.just_moved_two and board[row + 1][col].piece.color != self.selected_piece.color:
        # Update the new square with the selected piece
        board[row][col].piece = self.selected_piece
        instance.text = self.selected_piece.name
        instance.color = self.selected_piece.color

        #Update the enemy pawn square
        board[row - 1][col].piece = None
        if board[row][col].column < self.selected_piece.column:
            self.buttons[self.index_of_selected_piece_button - 1].text = ""
        else:
            self.buttons[self.index_of_selected_piece_button + 1].text = ""
        
        # Update the selected piece with it's new row and column and has_moved property
        board[row][col].piece.row = board[row][col].row
        board[row][col].piece.column = board[row][col].column
        board[row][col].piece.has_moved = True
        board[row][col].can_au_passant = False

        # Update old square to no longer have a piece
        board[self.selected_row - 1][self.selected_column - 1].piece = None
        self.buttons[self.index_of_selected_piece_button].text = ""

        # Resets selected piece to nothing
        self.selected_piece = ""

        # Changes turn color
        if self.turn == "white":
            self.turn = "black"
            self.display_text = "Black's Turn"
            app.display.text = "Black's Turn"
        else:
            self.turn = "white"
            self.display_text = "White's Turn"
            app.display.text = "White's Turn"
                            

def execute_castling_logic(self, board, row, col, instance):
    if self.selected_piece.color == "white" and board[row][col].row == 1 and board[row][col].column == 7 and self.selected_piece.can_castle_kingside:
        # Update the new square with the selected piece
        board[row][col].piece = self.selected_piece
        instance.text = self.selected_piece.name
        instance.color = self.selected_piece.color

        #Update the new rook square
        board[row][col - 1].piece = Rook("Rook", "white", 1, 6, 5)
        board[row][col - 1].piece.has_moved = True
        self.buttons[self.index_of_selected_piece_button + 1].text = "Rook"

        #Update old rook square
        board[row][col + 1].piece = None
        self.buttons[self.index_of_selected_piece_button + 3].text = ""

        # Update the selected piece with it's new row and column and has_moved property
        board[row][col].piece.row = board[row][col].row
        board[row][col].piece.column = board[row][col].column
        board[row][col].piece.has_moved = True

        # Update old king square to no longer have a piece
        board[self.selected_row - 1][self.selected_column - 1].piece = None
        self.buttons[self.index_of_selected_piece_button].text = ""

        # Resets selected piece to nothing
        self.selected_piece = ""

        # Changes turn color
        if self.turn == "white":
            self.turn = "black"
            self.display_text = "Black's Turn"
            app.display.text = "Black's Turn"
        else:
            self.turn = "white"
            self.display_text = "White's Turn"
            app.display.text = "White's Turn"

    elif self.selected_piece.color == "white" and board[row][col].row == 1 and board[row][col].column == 3 and self.selected_piece.can_castle_queenside:
        # Update the new square with the selected piece
        board[row][col].piece = self.selected_piece
        instance.text = self.selected_piece.name
        instance.color = self.selected_piece.color

        #Update the new rook square
        board[row][col + 1].piece = Rook("Rook", "white", 1, 4, 5)
        board[row][col + 1].piece.has_moved = True
        self.buttons[self.index_of_selected_piece_button - 1].text = "Rook"

        #Update old rook square
        board[row][col - 2].piece = None
        self.buttons[self.index_of_selected_piece_button - 4].text = ""

        # Update the selected piece with it's new row and column and has_moved property
        board[row][col].piece.row = board[row][col].row
        board[row][col].piece.column = board[row][col].column
        board[row][col].piece.has_moved = True

        # Update old king square to no longer have a piece
        board[self.selected_row - 1][self.selected_column - 1].piece = None
        self.buttons[self.index_of_selected_piece_button].text = ""

        # Resets selected piece to nothing
        self.selected_piece = ""

        # Changes turn color
        if self.turn == "white":
            self.turn = "black"
            self.display_text = "Black's Turn"
            app.display.text = "Black's Turn"
        else:
            self.turn = "white"
            self.display_text = "White's Turn"
            app.display.text = "White's Turn"

    elif self.selected_piece.color == "black" and board[row][col].row == 8 and board[row][col].column == 7 and self.selected_piece.can_castle_kingside:
        # Update the new square with the selected piece
        board[row][col].piece = self.selected_piece
        instance.text = self.selected_piece.name
        instance.color = self.selected_piece.color

        #Update the new rook square
        board[row][col - 1].piece = Rook("Rook", "black", 8, 6, 5)
        board[row][col - 1].piece.has_moved = True
        self.buttons[self.index_of_selected_piece_button + 1].text = "Rook"

        #Update old rook square
        board[row][col + 1].piece = None
        self.buttons[self.index_of_selected_piece_button + 3].text = ""

        # Update the selected piece with it's new row and column and has_moved property
        board[row][col].piece.row = board[row][col].row
        board[row][col].piece.column = board[row][col].column
        board[row][col].piece.has_moved = True

        # Update old king square to no longer have a piece
        board[self.selected_row - 1][self.selected_column - 1].piece = None
        self.buttons[self.index_of_selected_piece_button].text = ""

        # Resets selected piece to nothing
        self.selected_piece = ""

        # Changes turn color
        if self.turn == "white":
            self.turn = "black"
            self.display_text = "Black's Turn"
            app.display.text = "Black's Turn"
        else:
            self.turn = "white"
            self.display_text = "White's Turn"
            app.display.text = "White's Turn"

    elif self.selected_piece.color == "black" and board[row][col].row == 8 and board[row][col].column == 3 and self.selected_piece.can_castle_queenside:
        # Update the new square with the selected piece
        board[row][col].piece = self.selected_piece
        instance.text = self.selected_piece.name
        instance.color = self.selected_piece.color

        #Update the new rook square
        board[row][col + 1].piece = Rook("Rook", "black", 8, 4, 5)
        board[row][col + 1].piece.has_moved = True
        self.buttons[self.index_of_selected_piece_button - 1].text = "Rook"

        #Update old rook square
        board[row][col - 2].piece = None
        self.buttons[self.index_of_selected_piece_button - 4].text = ""

        # Update the selected piece with it's new row and column and has_moved property
        board[row][col].piece.row = board[row][col].row
        board[row][col].piece.column = board[row][col].column
        board[row][col].piece.has_moved = True

        # Update old king square to no longer have a piece
        board[self.selected_row - 1][self.selected_column - 1].piece = None
        self.buttons[self.index_of_selected_piece_button].text = ""

        # Resets selected piece to nothing
        self.selected_piece = ""

        # Changes turn color
        if self.turn == "white":
            self.turn = "black"
            self.display_text = "Black's Turn"
            app.display.text = "Black's Turn"
        else:
            self.turn = "white"
            self.display_text = "White's Turn"
            app.display.text = "White's Turn"

def check_if_move_takes_out_of_check(self, board, row, col, piece):
    king = ""
    for row2 in range(8):
        for col2 in range(8):
            if board[row2][col2].piece:
                if board[row2][col2].piece.name == "King" and board[row2][col2].piece.color == self.turn:
                    king = board[row2][col2].piece
    board[row][col].holding_piece = board[row][col].piece
    board[row][col].piece = piece
    king.in_check = False
    if check_if_king_in_check(self, board, king):
        board[row][col].piece = board[row][col].holding_piece
        board[row][col].holding_piece = None
        return False
    else:
        board[row][col].piece = board[row][col].holding_piece
        board[row][col].holding_piece = None
        return True

def check_if_king_in_check(self, board, king):
    king.in_check = False
    # Check for knights in possible knight checking squares
    if king.row + 2 <= 8 and king.column + 1 <= 8 and board[king.row + 1][king.column].piece and board[king.row + 1][king.column].piece.name == "Knight" and board[king.row + 1][king.column].piece.color != king.color:
        king.in_check = True
        self.checking_pieces.append(board[king.row + 1][king.column].piece)
    if king.row + 2 <= 8 and king.column - 1 >= 1 and board[king.row + 1][king.column - 2].piece and board[king.row + 1][king.column - 2].piece.name == "Knight" and board[king.row + 1][king.column - 2].piece.color != king.color:
        king.in_check = True
        self.checking_pieces.append(board[king.row + 1][king.column - 2].piece)
    if king.row - 2 >= 1 and king.column + 1 <= 8 and board[king.row - 3][king.column].piece and board[king.row - 3][king.column].piece.name == "Knight" and board[king.row - 3][king.column].piece.color != king.color:
        king.in_check = True
        self.checking_pieces.append(board[king.row - 3][king.column].piece)
    if king.row - 2 >= 1 and king.column - 1 >= 1 and board[king.row - 3][king.column - 2].piece and board[king.row - 3][king.column - 2].piece.name == "Knight" and board[king.row - 3][king.column - 2].piece.color != king.color:
        king.in_check = True
        self.checking_pieces.append(board[king.row - 3][king.column - 2].piece)
    if king.row + 1 <= 8 and king.column + 2 <= 8 and board[king.row][king.column + 1].piece and board[king.row][king.column + 1].piece.name == "Knight" and board[king.row][king.column + 1].piece.color != king.color:
        king.in_check = True
        self.checking_pieces.append(board[king.row][king.column + 1].piece)
    if king.row + 1 <= 8 and king.column - 2 >= 1 and board[king.row][king.column - 3].piece and board[king.row][king.column - 3].piece.name == "Knight" and board[king.row][king.column - 3].piece.color != king.color:
        king.in_check = True
        self.checking_pieces.append(board[king.row][king.column - 3].piece)
    if king.row - 1 >= 1 and king.column + 2 <= 8 and board[king.row - 2][king.column + 1].piece and board[king.row - 2][king.column + 1].piece.name == "Knight" and board[king.row - 2][king.column + 1].piece.color != king.color:
        king.in_check = True
        self.checking_pieces.append(board[king.row - 2][king.column + 1].piece)
    if king.row - 1 >= 1 and king.column - 2 >= 1 and board[king.row - 2][king.column - 3].piece and board[king.row - 2][king.column - 3].piece.name == "Knight" and board[king.row - 2][king.column - 3].piece.color != king.color:
        king.in_check = True
        self.checking_pieces.append(board[king.row - 2][king.column - 3].piece)
    
    # Set the actual king square on the board to None, so it doesn't block potential checks
    for row in range(8):
        for col in range(8):
            if board[row][col].piece and board[row][col].piece.name == "King" and board[row][col].piece.color == king.color and (board[row][col].row != king.row or board[row][col].column != king.column):
                board[row][col].holding_piece = board[row][col].piece
                board[row][col].piece = None

    # Find all squares the king could be checked from (excluding knight which is checked above)
    king.calculate_possible_squares_to_be_checked_from()
    bishop_movement(self, board, king)
    rook_movement(self, board, king)
    

    # Check for rooks or queens in straight checking squares and Bishops and Queens on the diagonal
    for row in range(8):
        for col in range(8):
            if [board[row][col].row, board[row][col].column] in king.possible_squares_to_be_checked_from and board[row][col].piece and (board[row][col].piece.name == "Queen" or board[row][col].piece.name == "Rook") and (board[row][col].row == king.row or board[row][col].column == king.column) and board[row][col].piece.color != king.color:

                king.in_check = True
                self.checking_pieces.append(board[row][col].piece)
            if [board[row][col].row, board[row][col].column] in king.possible_squares_to_be_checked_from and board[row][col].piece and (board[row][col].piece.name == "Queen" or board[row][col].piece.name == "Bishop") and board[row][col].row != king.row and board[row][col].column != king.column and board[row][col].piece.color != king.color:
                king.in_check = True
                self.checking_pieces.append(board[row][col].piece)
            if king.color == "white" and [board[row][col].row, board[row][col].column] in king.possible_squares_to_be_checked_from and board[row][col].piece and board[row][col].piece.name == "Pawn" and board[row][col].row == king.row + 1 and (board[row][col].column == king.column + 1 or board[row][col].column == king.column - 1) and board[row][col].piece.color != king.color:
                king.in_check = True
                self.checking_pieces.append(board[row][col].piece)
            if king.color == "black" and [board[row][col].row, board[row][col].column] in king.possible_squares_to_be_checked_from and board[row][col].piece and board[row][col].piece.name == "Pawn" and board[row][col].row == king.row - 1 and (board[row][col].column == king.column + 1 or board[row][col].column == king.column - 1) and board[row][col].piece.color != king.color:
                king.in_check = True
                self.checking_pieces.append(board[row][col].piece)
            # Check for other king being able to check
            if [board[row][col].row, board[row][col].column] in king.possible_squares_to_be_checked_from and abs(king.row - board[row][col].row) <= 1 and abs(king.column - board[row][col].column) <= 1 and board[row][col].piece and board[row][col].piece.name == "King" and board[row][col].piece.color != king.color:
                king.in_check = True
                self.checking_pieces.append(board[row][col].piece)

    # Reset king on board after testing
    for row in range(8):
        for col in range(8):
            if board[row][col].holding_piece and board[row][col].holding_piece.name == "King" and board[row][col].holding_piece.color == king.color:
                board[row][col].piece = board[row][col].holding_piece
                board[row][col].holding_piece = None
    
    if king.in_check:
        return True


def check_for_checkmate(self, board, king):
    # Find where the king can move that won't be in check
    king.calculate_possible_moves()
    king_movement(self, board, king)
    moves_to_remove = []
    if king.possible_moves:
        for move in king.possible_moves:
            if check_if_king_in_check(self, board, King("King", king.color, move[0], move[1], 10, False)):
                moves_to_remove.append(move)

    for move in moves_to_remove:
            if move in king.possible_moves:
                king.possible_moves.remove(move)
    
    if king.possible_moves:
        print("King can move somewhere", king.possible_moves)
        return False
    
    # Find if any pieces can capture the checking piece
    self.checking_pieces = []
    check_if_king_in_check(self, board, king)
    if len(self.checking_pieces) < 2:
        for row in range(8):
            for col in range(8):
                if board[row][col].piece and board[row][col].piece.color == king.color and board[row][col].piece.name != "King":
                    board[row][col].piece.calculate_possible_moves()
                    if board[row][col].piece.name == "Pawn":
                        pawn_movement(self, board, board[row][col].piece)
                    if board[row][col].piece.name == "Bishop":
                        bishop_movement(self, board, board[row][col].piece)
                    if board[row][col].piece.name == "Rook":
                        rook_movement(self, board, board[row][col].piece)
                    if board[row][col].piece.name == "Queen":
                        rook_movement(self, board, board[row][col].piece)
                        bishop_movement(self, board, board[row][col].piece)
                    for move in board[row][col].piece.possible_moves:
                        if move[0] == self.checking_pieces[0].row and move[1] == self.checking_pieces[0].column:
                            print(board[row][col].piece.name)
                            print("Can take the piece")
                            return False
    
    # Find if any piece can move in the way of the check
    if len(self.checking_pieces) < 2 and self.checking_pieces[0].name != "Knight" and self.checking_pieces[0].name != "Pawn":
        for row in range(8):
            for col in range(8):
                if board[row][col].piece and board[row][col].piece.color == king.color and board[row][col].piece.name != "King":
                    # board[row][col].piece.possible_moves = []
                    board[row][col].piece.calculate_possible_moves()
                    if board[row][col].piece.name == "Pawn":
                        pawn_movement(self, board, board[row][col].piece)
                    if board[row][col].piece.name == "Bishop":
                        bishop_movement(self, board, board[row][col].piece)
                    if board[row][col].piece.name == "Rook":
                        rook_movement(self, board, board[row][col].piece)
                    if board[row][col].piece.name == "Queen":
                        rook_movement(self, board, board[row][col].piece)
                        bishop_movement(self, board, board[row][col].piece)
                    for square in king.possible_squares_to_be_checked_from:
                        if [square[0], square[1]] in board[row][col].piece.possible_moves and check_if_move_takes_out_of_check(self, board, square[0] - 1, square[1] - 1, board[row][col].piece):
                            # If moving the piece to that square makes it no longer a check
                            print("Can move piece in the way")
                            return False
    
    print("Checkmate!")
    self.turn = ""
    app.control_panel.add_widget(self.new_game)
    return True

def check_castling(self, board, king):
    if king.color == "white" and not king.has_moved:
        if board[0][5].piece == None and board[0][6].piece == None and not check_if_king_in_check(self, board, king) and not check_if_king_in_check(self, board, King("King", king.color, 1, 6, 10, False)) and not check_if_king_in_check(self, board, King("King", king.color, 1, 7, 10, False)):
            for row in range(8):
                for col in range(8):
                    if board[row][col].piece and board[row][col].piece.name == "Rook" and board[row][col].piece.color == king.color and board[row][col].piece.has_moved == False and board[row][col].column == 8:
                        print("White can castle king side")
                        king.can_castle_kingside = True
        if board[0][1].piece == None and board[0][2].piece == None and board[0][3].piece == None and not check_if_king_in_check(self, board, king) and not check_if_king_in_check(self, board, King("King", king.color, 1, 3, 10, False)) and not check_if_king_in_check(self, board, King("King", king.color, 1, 4, 10, False)):
            for row in range(8):
                for col in range(8):
                    if board[row][col].piece and board[row][col].piece.name == "Rook" and board[row][col].piece.color == king.color and board[row][col].piece.has_moved == False and board[row][col].column == 1:
                        print("White can castle queen side")
                        king.can_castle_queenside = True
    if king.color == "black" and not king.has_moved:
        if board[7][5].piece == None and board[7][6].piece == None and not check_if_king_in_check(self, board, king) and not check_if_king_in_check(self, board, King("King", king.color, 8, 6, 10, False)) and not check_if_king_in_check(self, board, King("King", king.color, 8, 7, 10, False)):
            for row in range(8):
                for col in range(8):
                    if board[row][col].piece and board[row][col].piece.name == "Rook" and board[row][col].piece.color == king.color and board[row][col].piece.has_moved == False and board[row][col].column == 8:
                        print("Black can castle king side")
                        king.can_castle_kingside = True
        if board[7][1].piece == None and board[7][2].piece == None and board[7][3].piece == None and not check_if_king_in_check(self, board, king) and not check_if_king_in_check(self, board, King("King", king.color, 8, 3, 10, False)) and not check_if_king_in_check(self, board, King("King", king.color, 8, 4, 10, False)):
            for row in range(8):
                for col in range(8):
                    if board[row][col].piece and board[row][col].piece.name == "Rook" and board[row][col].piece.color == king.color and board[row][col].piece.has_moved == False and board[row][col].column == 1:
                        print("Black can castle queen side")
                        king.can_castle_queenside = True

def king_movement(self, board, given_piece):
    moves_to_remove = []
    for row in range(8):
        for col in range(8):
            if [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[row][col].piece and board[row][col].piece.color == given_piece.color:
                moves_to_remove.append([board[row][col].row, board[row][col].column])
    
    for move in moves_to_remove:
            if move in given_piece.possible_moves:
                given_piece.possible_moves.remove(move)

    if given_piece.possible_moves:
        for move in given_piece.possible_moves:
            if check_if_king_in_check(self, board, King("King", given_piece.color, move[0], move[1], 10, False)):
                moves_to_remove.append(move)
    
    for move in moves_to_remove:
            if move in given_piece.possible_moves:
                given_piece.possible_moves.remove(move)

def pawn_movement(self, board, given_piece):
    given_piece.can_au_passant = False
    moves_to_remove = []
    for row in range(8):
        for col in range(8):
            if given_piece.color == "white" and [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[row][col].column != given_piece.column and (not board[row][col].piece or board[row][col].piece.color == given_piece.color):
                #Au Passant logic (don't remove move if au passant is possible)
                if board[row - 1][col].piece and board[row - 1][col].piece.name == "Pawn" and board[row - 1][col].piece.just_moved_two and board[row - 1][col].piece.color != given_piece.color:
                    given_piece.can_au_passant = True
                else:
                    moves_to_remove.append([board[row][col].row, board[row][col].column])
            if given_piece.color == "white" and [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[row][col].column == given_piece.column and board[given_piece.row][given_piece.column - 1].piece:
                moves_to_remove.append([board[row][col].row, board[row][col].column])
            if given_piece.color == "white" and not given_piece.has_moved and [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[given_piece.row + 1][given_piece.column - 1].piece and board[row][col].row - 2 == given_piece.row:
                moves_to_remove.append([board[row][col].row, board[row][col].column])
            if given_piece.color == "black" and [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[row][col].column != given_piece.column and (not board[row][col].piece or board[row][col].piece.color == given_piece.color):
                #Au Passant logic (don't remove move if au passant is possible)
                if board[row + 1][col].piece and board[row + 1][col].piece.name == "Pawn" and board[row + 1][col].piece.just_moved_two and board[row + 1][col].piece.color != given_piece.color:
                    given_piece.can_au_passant = True
                else:
                    moves_to_remove.append([board[row][col].row, board[row][col].column])
            if given_piece.color == "black" and [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[row][col].column == given_piece.column and board[given_piece.row - 2][given_piece.column - 1].piece:
                moves_to_remove.append([board[row][col].row, board[row][col].column])
            if given_piece.color == "black" and not given_piece.has_moved and [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[given_piece.row - 3][given_piece.column - 1].piece and board[row][col].row + 2 == given_piece.row:
                moves_to_remove.append([board[row][col].row, board[row][col].column])
    
    for move in moves_to_remove:
            if move in given_piece.possible_moves:
                given_piece.possible_moves.remove(move)


def rook_movement(self, board, given_piece):
    # Remove possible moves if a piece is in the way

    # Find all of the pieces in the rooks' movement squares
    # Reusable to find enemy pieces that can check the king 
    all_pieces_in_the_way = []
    if given_piece.name == "King":
        for row in range(8):
            for col in range(8):
                if [board[row][col].row, board[row][col].column] in given_piece.possible_squares_to_be_checked_from and board[row][col].piece:
                    all_pieces_in_the_way.append([board[row][col].row, board[row][col].column, board[row][col].piece.color])
    else:
        for row in range(8):
            for col in range(8):
                if [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[row][col].piece:
                    all_pieces_in_the_way.append([board[row][col].row, board[row][col].column, board[row][col].piece.color])
    
    # Split up all of the pieces based on the direction in relation to the rook
    all_pieces_above = list(filter(lambda piece: piece[1] == given_piece.column and piece[0] - given_piece.row > 0, all_pieces_in_the_way))
    all_pieces_below = list(filter(lambda piece: piece[1] == given_piece.column and piece[0] - given_piece.row < 0, all_pieces_in_the_way))
    all_pieces_right = list(filter(lambda piece: piece[0] == given_piece.row and piece[1] - given_piece.column > 0, all_pieces_in_the_way))
    all_pieces_left = list(filter(lambda piece: piece[0] == given_piece.row and piece[1] - given_piece.column < 0, all_pieces_in_the_way))

    # Find the closest piece to the rook in each direction
    if len(all_pieces_above) > 0:
        closest_piece_above = min(all_pieces_above, key=lambda piece: abs(given_piece.row - piece[0]))
    else:
        closest_piece_above = []
    
    if len(all_pieces_below) > 0:
        closest_piece_below = min(all_pieces_below, key=lambda piece: abs(given_piece.row - piece[0]))
    else:
        closest_piece_below = []

    if len(all_pieces_right) > 0:
        closest_piece_right = min(all_pieces_right, key=lambda piece: abs(given_piece.column - piece[1]))
    else:
        closest_piece_right = []
    
    if len(all_pieces_left) > 0:
        closest_piece_left = min(all_pieces_left, key=lambda piece: abs(given_piece.column - piece[1]))
    else:
        closest_piece_left = []

    # Find and remove all moves that are past the closest piece to the rook
    # Reusable to find enemy pieces that can check the king
    moves_to_remove = []

    if given_piece.name == "King":
        for move in given_piece.possible_squares_to_be_checked_from:
            if len(closest_piece_above) > 0:
                if move[1] == closest_piece_above[1] and move[0] > closest_piece_above[0]:
                    moves_to_remove.append(move)
                if closest_piece_above[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_above[0], closest_piece_above[1]])
            
            if len(closest_piece_below) > 0:
                if move[1] == closest_piece_below[1] and move[0] < closest_piece_below[0]:
                    moves_to_remove.append(move)
                if closest_piece_below[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_below[0], closest_piece_below[1]])
            
            if len(closest_piece_right) > 0:
                if move[0] == closest_piece_right[0] and move[1] > closest_piece_right[1]:
                    moves_to_remove.append(move)
                if closest_piece_right[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_right[0], closest_piece_right[1]])

            if len(closest_piece_left) > 0:
                if move[0] == closest_piece_left[0] and move[1] < closest_piece_left[1]:
                    moves_to_remove.append(move)
                if closest_piece_left[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_left[0], closest_piece_left[1]])
        
        for move in moves_to_remove:
            if move in given_piece.possible_squares_to_be_checked_from:
                given_piece.possible_squares_to_be_checked_from.remove(move)
    else:
        for move in given_piece.possible_moves:
            if len(closest_piece_above) > 0:
                if move[1] == closest_piece_above[1] and move[0] > closest_piece_above[0]:
                    moves_to_remove.append(move)
                if closest_piece_above[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_above[0], closest_piece_above[1]])
            
            if len(closest_piece_below) > 0:
                if move[1] == closest_piece_below[1] and move[0] < closest_piece_below[0]:
                    moves_to_remove.append(move)
                if closest_piece_below[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_below[0], closest_piece_below[1]])
            
            if len(closest_piece_right) > 0:
                if move[0] == closest_piece_right[0] and move[1] > closest_piece_right[1]:
                    moves_to_remove.append(move)
                if closest_piece_right[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_right[0], closest_piece_right[1]])

            if len(closest_piece_left) > 0:
                if move[0] == closest_piece_left[0] and move[1] < closest_piece_left[1]:
                    moves_to_remove.append(move)
                if closest_piece_left[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_left[0], closest_piece_left[1]])
        
        for move in moves_to_remove:
            if move in given_piece.possible_moves:
                given_piece.possible_moves.remove(move)

def bishop_movement(self, board, given_piece):
    # Remove possible moves if a piece is in the way

    # Find all of the pieces in the bishop's movement squares
    # Reusable to find enemy pieces that can check the king
    all_pieces_in_the_way = []
    if given_piece.name == "King":
        for row in range(8):
            for col in range(8):
                if [board[row][col].row, board[row][col].column] in given_piece.possible_squares_to_be_checked_from and board[row][col].piece:
                    all_pieces_in_the_way.append([board[row][col].row, board[row][col].column, board[row][col].piece.color])
    else:
        for row in range(8):
            for col in range(8):
                if [board[row][col].row, board[row][col].column] in given_piece.possible_moves and board[row][col].piece:
                    all_pieces_in_the_way.append([board[row][col].row, board[row][col].column, board[row][col].piece.color])

    # Split up all of the pieces based on the direction in relation to the bishop
    all_pieces_up_right = list(filter(lambda piece: piece[0] > given_piece.row and piece[1] > given_piece.column, all_pieces_in_the_way))
    all_pieces_up_left = list(filter(lambda piece: piece[0] > given_piece.row and piece[1] < given_piece.column, all_pieces_in_the_way))
    all_pieces_down_right = list(filter(lambda piece: piece[0] < given_piece.row and piece[1] > given_piece.column, all_pieces_in_the_way))
    all_pieces_down_left = list(filter(lambda piece: piece[0] < given_piece.row and piece[1] < given_piece.column, all_pieces_in_the_way))


    # Find the closest piece to the bishiop in each direction
    if len(all_pieces_up_right) > 0:
        closest_piece_up_right = min(all_pieces_up_right, key=lambda piece: abs(given_piece.row - piece[0]))
    else:
        closest_piece_up_right = []
    
    if len(all_pieces_up_left) > 0:
        closest_piece_up_left = min(all_pieces_up_left, key=lambda piece: abs(given_piece.row - piece[0]))
    else:
        closest_piece_up_left = []
    
    if len(all_pieces_down_right) > 0:
        closest_piece_down_right = min(all_pieces_down_right, key=lambda piece: abs(given_piece.row - piece[0]))
    else:
        closest_piece_down_right = []
    
    if len(all_pieces_down_left) > 0:
        closest_piece_down_left = min(all_pieces_down_left, key=lambda piece: abs(given_piece.row - piece[0]))
    else:
        closest_piece_down_left = []
    
    # Find and remove all moves that are past the closet piece to the bishop
    # Reusable to find enemy pieces that can check the king
    moves_to_remove = []

    if given_piece.name == "King":
        for move in given_piece.possible_squares_to_be_checked_from:
            if len(closest_piece_up_right) > 0:
                if move[0] > closest_piece_up_right[0] and move[1] > closest_piece_up_right[1]:
                    moves_to_remove.append(move)
                if closest_piece_up_right[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_up_right[0], closest_piece_up_right[1]])
            
            if len(closest_piece_up_left) > 0:
                if move[0] > closest_piece_up_left[0] and move[1] < closest_piece_up_left[1]:
                    moves_to_remove.append(move)
                if closest_piece_up_left[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_up_left[0], closest_piece_up_left[1]])

            if len(closest_piece_down_right) > 0:
                if move[0] < closest_piece_down_right[0] and move[1] > closest_piece_down_right[1]:
                    moves_to_remove.append(move)
                if closest_piece_down_right[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_down_right[0], closest_piece_down_right[1]])
            
            if len(closest_piece_down_left) > 0:
                if move[0] < closest_piece_down_left[0] and move[1] < closest_piece_down_left[1]:
                    moves_to_remove.append(move)
                if closest_piece_down_left[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_down_left[0], closest_piece_down_left[1]])
        
        for move in moves_to_remove:
            if move in given_piece.possible_squares_to_be_checked_from:
                given_piece.possible_squares_to_be_checked_from.remove(move)
    else:
        for move in given_piece.possible_moves:
            if len(closest_piece_up_right) > 0:
                if move[0] > closest_piece_up_right[0] and move[1] > closest_piece_up_right[1]:
                    moves_to_remove.append(move)
                if closest_piece_up_right[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_up_right[0], closest_piece_up_right[1]])
            
            if len(closest_piece_up_left) > 0:
                if move[0] > closest_piece_up_left[0] and move[1] < closest_piece_up_left[1]:
                    moves_to_remove.append(move)
                if closest_piece_up_left[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_up_left[0], closest_piece_up_left[1]])

            if len(closest_piece_down_right) > 0:
                if move[0] < closest_piece_down_right[0] and move[1] > closest_piece_down_right[1]:
                    moves_to_remove.append(move)
                if closest_piece_down_right[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_down_right[0], closest_piece_down_right[1]])
            
            if len(closest_piece_down_left) > 0:
                if move[0] < closest_piece_down_left[0] and move[1] < closest_piece_down_left[1]:
                    moves_to_remove.append(move)
                if closest_piece_down_left[2] == given_piece.color:
                    moves_to_remove.append([closest_piece_down_left[0], closest_piece_down_left[1]])
        
        for move in moves_to_remove:
            if move in given_piece.possible_moves:
                given_piece.possible_moves.remove(move)



if __name__ == "__main__":
    app = MainApp()
    app.run()
