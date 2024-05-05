from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from tensorflow import keras
from kivy.uix.boxlayout import BoxLayout
import numpy
import json
import random
from kivy.core.window import Window
from kivy.metrics import dp

board_stats = {}  # Define board_stats as a global variable


class InstructionBoard(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1  # Set the number of columns to the number of buttons
        self.rows = 20  # Adjusted rows to accommodate the instruction labels and "Next" button

        # Add buttons
        self.add_buttons()

    def add_buttons(self):
        button_size = (dp(300), dp(200))  # Adjust button size as needed
        self.TwoPlayers_button = Button(text="Two Players", font_size=dp(24), size_hint=(None, None), size=button_size)
        self.RandomCompute_button = Button(text="Random Computer", font_size=dp(24), size_hint=(None, None),
                                           size=button_size)
        self.SmartComputer_button = Button(text="Smart Computer", font_size=dp(24), size_hint=(None, None),
                                           size=button_size)
        self.NeuralSystem_button = Button(text="Neural System", font_size=dp(24), size_hint=(None, None),
                                          size=button_size)

        # Add buttons to the layout
        self.add_widget(self.TwoPlayers_button)
        self.add_widget(self.RandomCompute_button)
        self.add_widget(self.SmartComputer_button)
        self.add_widget(self.NeuralSystem_button)

class TwoPlayers(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 3
        self.buttons = []
        self.all_pieces_placed = False
        self.selected_piece = None
        self.remaining_pieces = {'X': 3, 'O': 3}
        self.current_player = random.choice(['X', 'O'])  # Randomly choose starting player

        for i in range(9):
            button = Button(text='', font_size=24, size_hint=(None, None), width=300, height=300)
            button.bind(on_press=self.on_button_click)
            self.buttons.append(button)
            self.add_widget(button)

    def on_button_click(self, button):

        if not self.all_pieces_placed:
            # Placing phase
            if button.text == '':
                if self.remaining_pieces[self.current_player] > 0:
                    button.text = self.current_player
                    self.remaining_pieces[self.current_player] -= 1

                    # Check for winner after placing a piece
                    if self.check_winner(self.current_player):
                        winner = 'O' if self.current_player == 'O' else 'X'
                        self.show_message('Congratulations!', f'{winner} wins!')
                        return  # Stop further actions if there's a winner

                    self.current_player = 'O' if self.current_player == 'X' else 'X'

                    if all(self.remaining_pieces[player] == 0 for player in ['X', 'O']):
                        self.all_pieces_placed = True

                else:
                    self.show_message('Error', 'You have no more pieces left.')
                    self.current_player = 'X' if self.current_player == 'X' else 'O'  # Switch to the next player for moving phase
            else:
                self.show_message('Error', 'This position is already occupied.')

        else:
            # Moving phase
            if self.selected_piece is None:
                # Selecting a piece to move
                if button.text == self.current_player:
                    self.selected_piece = button
                    button.background_color = (0, 1, 0, 1)  # Highlight selected piece
                else:
                    self.show_message('Error', 'You can only move your own pieces.')

            else:
                # Unselecting the selected piece
                if button is self.selected_piece:
                    self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                    self.selected_piece = None
                    return  # Stop further actions

                # Moving the selected piece
                if button.text == '':
                    # Calculate distance between selected piece and target position
                    nearby_places = []
                    selected_index = self.buttons.index(self.selected_piece)
                    target_index = self.buttons.index(button)
                    nearby_places = self.available_positions_to(selected_index)

                    if target_index in nearby_places:
                        # Move the piece to the target position
                        button.text = self.selected_piece.text
                        self.selected_piece.text = ''
                        self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                        self.selected_piece = None

                        # Check for winner after moving a piece
                        if self.check_winner(self.current_player):
                            winner = 'O' if self.current_player == 'O' else 'X'
                            self.show_message('Congratulations!', f'{winner} wins!')
                        else:
                            # Switch current player
                            self.current_player = 'O' if self.current_player == 'X' else 'X'
                    else:
                        self.show_message('Error', 'You can only move your piece to a nearby position.')

                else:
                    self.show_message('Error', 'You can only move your piece to an empty position.')

    def available_positions_to(self, from_index):
        row = from_index // 3
        col = from_index % 3

        nearby_places = []

        for i in range(max(0, row - 1), min(3, row + 2)):
            for j in range(max(0, col - 1), min(3, col + 2)):
                nearby_index = i * 3 + j
                if self.is_valid_index(nearby_index) and self.buttons[nearby_index].text == '':
                    nearby_places.append(nearby_index)

        return nearby_places

    def is_valid_index(self, index):
        return 0 <= index < 9

    def check_winner(self, symbol):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for combination in winning_combinations:
            if all(self.buttons[i].text == symbol for i in combination):
                return True  # Found a winning combination

        return False  # No winning combination found

    def show_message(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200)).open()


class RandomComputer(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 3
        self.buttons = []
        self.all_pieces_placed = False
        self.selected_piece = None
        self.remaining_pieces = {'X': 3, 'O': 2}
        self.current_player = 'X'

        for i in range(9):
            button = Button(text='', font_size=24, size_hint=(None, None), width=300, height=300)
            button.bind(on_press=self.on_button_click)
            self.buttons.append(button)
            self.add_widget(button)

    def on_button_click(self, button):
        if not self.all_pieces_placed:
            # Placing phase
            if button.text == '':
                if self.remaining_pieces[self.current_player] > 0:
                    button.text = self.current_player
                    selected_index = self.buttons.index(button)
                    self.remaining_pieces[self.current_player] -= 1

                    # Check for winner after placing a piece
                    if self.check_winner("X"):
                        self.show_message('Congratulations!', 'player wins!')
                        return  # Stop further actions if there's a winner

                    self.current_player = 'O' if self.current_player == 'X' else 'X'

                    if all(self.remaining_pieces[player] == 0 for player in ['X', 'O']):
                        self.all_pieces_placed = True

                    if self.current_player == 'O':
                        # If it's computer's turn, make its move
                        self.computer_place()
                        self.remaining_pieces['O'] -= 1

                else:
                    self.show_message('Error', 'You have no more pieces left.')
                    self.current_player = 'X' if self.current_player == 'X' else 'O'  # Switch to the next player for moving phase
            else:
                self.show_message('Error', 'This position is already occupied.')

        else:
            # Moving phase
            if self.selected_piece is None:
                # Selecting a piece to move
                if button.text == self.current_player:
                    self.selected_piece = button
                    button.background_color = (0, 1, 0, 1)  # Highlight selected piece
                else:
                    self.show_message('Error', 'You can only move your own pieces.')

            else:
                # Unselecting the selected piece
                if button is self.selected_piece:
                    self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                    self.selected_piece = None
                    return  # Stop further actions

                # Moving the selected piece
                if button.text == '':
                    # Calculate distance between selected piece and target position
                    selected_index = self.buttons.index(self.selected_piece)
                    target_index = self.buttons.index(button)
                    nearby_places = self.available_positions_to(selected_index)

                    if target_index in nearby_places:
                        # Move the piece to the target position
                        button.text = self.selected_piece.text
                        self.selected_piece.text = ''
                        self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                        self.selected_piece = None

                        # Check for winner after moving a piece
                        if self.check_winner("X"):
                            self.show_message('Congratulations!', 'Player wins!')
                        else:
                            # Switch current player
                            self.current_player = 'O'
                            if self.current_player == 'O':
                                # If it's computer's turn, make its move
                                self.computer_turn()

                    else:
                        self.show_message('Error', 'You can only move your piece to a nearby position.')

                else:
                    self.show_message('Error', 'You can only move your piece to an empty position.')

    def computer_place(self):
        empty_indices = [i for i, button in enumerate(self.buttons) if button.text == '']
        if empty_indices:
            # Choose a random empty spot for the computer's move
            index = random.choice(empty_indices)

            self.buttons[index].text = 'O'

            # Check for winner after computer's move
            if self.check_winner("O"):
                self.show_message('OutMatched!', 'Computer wins!')
            else:
                # Switch current player
                self.current_player = 'X'

    def computer_turn(self):
        # Find all buttons with 'O' text (computer's pieces)
        computer_pieces = [button for button in self.buttons if button.text == 'O']

        if computer_pieces:
            # Choose a random piece
            selected_piece = random.choice(computer_pieces)

            # Find the index of the selected piece
            selected_index = self.buttons.index(selected_piece)

            # Find nearby empty places for the selected piece
            nearby_empty_places = self.available_positions_to(selected_index)
            while not nearby_empty_places:
                # Choose a random piece
                selected_piece = random.choice(computer_pieces)

                # Find the index of the selected piece
                selected_index = self.buttons.index(selected_piece)

                # Find nearby empty places for the selected piece
                nearby_empty_places = self.available_positions_to(selected_index)

            if nearby_empty_places:
                # Choose a random nearby empty place
                target_index = random.choice(nearby_empty_places)

                # Move the piece to the target position
                self.buttons[target_index].text = selected_piece.text
                selected_piece.text = ''

                # Reset color (assuming you change the color when a piece is selected)
                selected_piece.background_color = (1, 1, 1, 1)  # Reset color

                if self.check_winner("O"):
                    self.show_message('OutMatched!', 'Computer wins!')
                else:
                    # Switch current player
                    self.current_player = 'X'

    def available_positions_to(self, from_index):
        row = from_index // 3
        col = from_index % 3

        nearby_places = []

        for i in range(max(0, row - 1), min(3, row + 2)):
            for j in range(max(0, col - 1), min(3, col + 2)):
                nearby_index = i * 3 + j
                if self.is_valid_index(nearby_index) and self.buttons[nearby_index].text == '':
                    nearby_places.append(nearby_index)

        return nearby_places

    def is_valid_index(self, index):
        return 0 <= index < 9

    def check_winner(self, symbol):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for combination in winning_combinations:
            if all(self.buttons[i].text == symbol for i in combination):
                return True  # Found a winning combination

        return False  # No winning combination found

    def show_message(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200)).open()


class SmartComputer(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_from_json()
        self.rows = 3
        self.cols = 3
        self.buttons = []
        self.all_pieces_placed = False
        self.selected_piece = None
        self.remaining_pieces = {'X': 3, 'O': 2}
        self.current_player = 'X'
        self.game_board = "000000000"
        self.game_board_history = [self.game_board]

        for i in range(9):
            button = Button(text='', font_size=24, size_hint=(None, None), width=300, height=300)
            button.bind(on_press=self.on_button_click)
            self.buttons.append(button)
            self.add_widget(button)

    def on_button_click(self, button):
        if not self.all_pieces_placed:
            # Placing phase
            if button.text == '':
                if self.remaining_pieces[self.current_player] > 0:
                    button.text = self.current_player
                    selected_index = self.buttons.index(button)
                    self.game_board = self.game_board[:selected_index] + "X" + self.game_board[selected_index + 1:]
                    self.game_board_history.append(self.game_board)
                    self.remaining_pieces[self.current_player] -= 1

                    # Check for winner after placing a piece
                    if self.check_winner("X"):
                        self.show_message('Congratulations!', 'player wins!')
                        return  # Stop further actions if there's a winner

                    self.current_player = 'O' if self.current_player == 'X' else 'X'

                    if all(self.remaining_pieces[player] == 0 for player in ['X', 'O']):
                        self.all_pieces_placed = True

                    if self.current_player == 'O':
                        # If it's computer's turn, make its move
                        self.place_best_position()
                        self.remaining_pieces['O'] -= 1

                else:
                    self.show_message('Error', 'You have no more pieces left.')
                    self.current_player = 'X' if self.current_player == 'X' else 'O'  # Switch to the next player for moving phase
            else:
                self.show_message('Error', 'This position is already occupied.')

        else:
            # Moving phase
            if self.selected_piece is None:
                # Selecting a piece to move
                if button.text == self.current_player:
                    self.selected_piece = button
                    button.background_color = (0, 1, 0, 1)  # Highlight selected piece
                else:
                    self.show_message('Error', 'You can only move your own pieces.')

            else:
                # Unselecting the selected piece
                if button is self.selected_piece:
                    self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                    self.selected_piece = None
                    return  # Stop further actions

                # Moving the selected piece
                if button.text == '':
                    # Calculate distance between selected piece and target position
                    selected_index = self.buttons.index(self.selected_piece)
                    target_index = self.buttons.index(button)
                    nearby_places = self.available_positions_to(selected_index)

                    if target_index in nearby_places:
                        # Move the piece to the target position
                        button.text = self.selected_piece.text
                        self.selected_piece.text = ''
                        self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                        self.update_board(selected_index, "0")
                        self.update_board(target_index, "X")
                        self.selected_piece = None

                        # Check for winner after moving a piece
                        if self.check_winner("X"):
                            self.show_message('Congratulations!', 'Player wins!')
                        else:
                            # Switch current player
                            self.current_player = 'O'
                            if self.current_player == 'O':
                                # If it's computer's turn, make its move
                                self.play_best_position()

                    else:
                        self.show_message('Error', 'You can only move your piece to a nearby position.')

                else:
                    self.show_message('Error', 'You can only move your piece to an empty position.')

    def place_best_position(self):
        available_positions = [i for i, char in enumerate(self.game_board) if char == "0"]

        best_position = None
        max_score = -1

        for position in available_positions:
            next_board = self.game_board[:position] + "O" + self.game_board[position + 1:]
            if (next_board not in board_stats):
                score = 0
            else:
                score, _ = board_stats[next_board]
            print(next_board, score)
            if score > max_score:
                max_score = score
                best_position = position

        # If max_score is 0, all the game board are not found.
        # placing the piece based on the maximum amount of pieces in a row, column, diagonal, or anti-diagonal
        if max_score == 0:
            max_piece_count = -1
            for position in available_positions:
                next_board = self.game_board[:position] + "O" + self.game_board[position + 1:]
                piece_count = self.max_count_in_line(next_board, "O")
                if piece_count > max_piece_count:
                    max_piece_count = piece_count
                    best_position = position

        self.buttons[best_position].text = 'O'
        self.update_board(best_position, "O")

        if self.check_winner("O"):
            self.show_message('OutMatched!', 'computer wins!')
        else:
            # Switch current player
            self.current_player = 'X'

    def play_best_position(self):
        available_positions = [i for i, char in enumerate(self.game_board) if char == "O"]

        best_position = None
        max_score = -1

        for position in available_positions:
            nearby_places = self.available_positions_to(position)
            for pos in nearby_places:
                nex_board = self.game_board[:position] + "0" + self.game_board[position + 1:]
                next_board = nex_board[:pos] + "O" + nex_board[pos + 1:]
                if (next_board not in board_stats):
                    score = 0
                else:
                    (score, _) = board_stats[next_board]
                if score > max_score:
                    from_index = position
                    max_score = score
                    best_position = pos

        # If max_score is 0, all the game boards are not found.
        # placing the piece based on the maximum amount of pieces in a row, column, diagonal, or anti-diagonal
        if max_score == 0:
            max_piece_count = -1
            for position in available_positions:
                nearby_places = self.available_positions_to(position)
                for pos in nearby_places:
                    nex_board = self.game_board[:position] + "0" + self.game_board[position + 1:]
                    next_board = nex_board[:pos] + "O" + nex_board[pos + 1:]
                    piece_count = self.max_count_in_line(next_board, "O")
                    if piece_count > max_piece_count:
                        from_index = position
                        max_piece_count = piece_count
                        best_position = pos

        self.buttons[from_index].text = ''
        self.buttons[best_position].text = 'O'
        self.update_board(from_index, '0')
        self.update_board(best_position, "O")

        if self.check_winner("O"):
            self.show_message('OutMatched!', 'computer wins!')
        else:
            # Switch current player
            self.current_player = 'X'

    def max_count_in_line(self, board, symbol):
        max_count = 0
        for i in range(len(board)):
            row, col = divmod(i, 3)
            # Check horizontal line
            count = sum(1 for j in range(3) if board[row * 3 + j] == symbol)
            max_count = max(max_count, count)
            # Check vertical line
            count = sum(1 for j in range(3) if board[j * 3 + col] == symbol)
            max_count = max(max_count, count)
            # Check main diagonal
            if row == col:
                count = sum(1 for j in range(3) if board[j * 3 + j] == symbol)
                max_count = max(max_count, count)
            # Check anti-diagonal
            if row + col == 2:
                count = sum(1 for j in range(3) if board[j * 3 + (2 - j)] == symbol)
                max_count = max(max_count, count)
        return max_count


    def available_positions_to(self, from_index):
        row = from_index // 3
        col = from_index % 3

        nearby_places = []

        for i in range(max(0, row - 1), min(3, row + 2)):
            for j in range(max(0, col - 1), min(3, col + 2)):
                nearby_index = i * 3 + j
                if self.is_valid_index(nearby_index) and self.buttons[nearby_index].text == '':
                    nearby_places.append(nearby_index)

        return nearby_places

    def is_valid_index(self, index):
        return 0 <= index < 9

    def check_winner(self, symbol):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]

        for combo in winning_combinations:
            if all(self.game_board[i] == symbol for i in combo):
                return True
        return False

    def load_from_json(self):
        global board_stats  # Use the global board_stats variable
        board_stats_file = "dict2.json"
        try:
            with open(board_stats_file, 'r') as json_file:
                board_stats = json.load(json_file)
        except FileNotFoundError:
            board_stats = {}

    def update_board(self, index, symbol):
        self.game_board = self.game_board[:index] + symbol + self.game_board[index + 1:]
        self.game_board_history.append(self.game_board)

    def show_message(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200)).open()


class NeuralSystem(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 3
        self.buttons = []
        self.all_pieces_placed = False
        self.selected_piece = None
        self.remaining_pieces = {'X': 3, 'O': 2}
        self.current_player = 'X'
        self.game_board = "000000000"
        self.game_board_history = [self.game_board]

        for i in range(9):
            button = Button(text='', font_size=24, size_hint=(None, None), width=300, height=300)
            button.bind(on_press=self.on_button_click)
            self.buttons.append(button)
            self.add_widget(button)

    def on_button_click(self, button):
        if not self.all_pieces_placed:
            # Placing phase
            if button.text == '':
                if self.remaining_pieces[self.current_player] > 0:
                    button.text = self.current_player
                    selected_index = self.buttons.index(button)
                    self.game_board = self.game_board[:selected_index] + "X" + self.game_board[selected_index + 1:]
                    self.game_board_history.append(self.game_board)
                    self.remaining_pieces[self.current_player] -= 1

                    # Check for winner after placing a piece
                    if self.check_winner("X"):
                        self.show_message('Congratulations!', 'player wins!')
                        return  # Stop further actions if there's a winner

                    self.current_player = 'O' if self.current_player == 'X' else 'X'

                    if all(self.remaining_pieces[player] == 0 for player in ['X', 'O']):
                        self.all_pieces_placed = True

                    if self.current_player == 'O':
                        # If it's computer's turn, make its move
                        self.place_best_position()
                        self.remaining_pieces['O'] -= 1

                else:
                    self.show_message('Error', 'You have no more pieces left.')
                    self.current_player = 'X' if self.current_player == 'X' else 'O'  # Switch to the next player for moving phase
            else:
                self.show_message('Error', 'This position is already occupied.')

        else:
            # Moving phase
            if self.selected_piece is None:
                # Selecting a piece to move
                if button.text == self.current_player:
                    self.selected_piece = button
                    button.background_color = (0, 1, 0, 1)  # Highlight selected piece
                else:
                    self.show_message('Error', 'You can only move your own pieces.')

            else:
                # Unselecting the selected piece
                if button is self.selected_piece:
                    self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                    self.selected_piece = None
                    return  # Stop further actions

                # Moving the selected piece
                if button.text == '':
                    # Calculate distance between selected piece and target position
                    selected_index = self.buttons.index(self.selected_piece)
                    target_index = self.buttons.index(button)
                    nearby_places = self.available_positions_to(selected_index)

                    if target_index in nearby_places:
                        # Move the piece to the target position
                        button.text = self.selected_piece.text
                        self.selected_piece.text = ''
                        self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                        self.update_board(selected_index, "0")
                        self.update_board(target_index, "X")
                        self.selected_piece = None

                        # Check for winner after moving a piece
                        if self.check_winner("X"):
                            self.show_message('Congratulations!', 'Player wins!')
                        else:
                            # Switch current player
                            self.current_player = 'O'
                            if self.current_player == 'O':
                                # If it's computer's turn, make its move
                                self.play_best_position()

                    else:
                        self.show_message('Error', 'You can only move your piece to a nearby position.')

                else:
                    self.show_message('Error', 'You can only move your piece to an empty position.')

    def place_best_position(self):
        available_positions = [i for i, char in enumerate(self.game_board) if char == "0"]

        best_position = None
        max_score = -1
        model2 = keras.models.load_model('saved model2.keras')
        two_dimensional_array = numpy.zeros((3, 3), int)

        for position in available_positions:
            next_board = self.game_board[:position] + "O" + self.game_board[position + 1:]

            k = 0
            j = 0
            i = 0
            while i < 9:
                if (next_board[i] == 'X'):
                    two_dimensional_array[k][j] = 1
                elif (next_board[i] == 'O'):
                    two_dimensional_array[k][j] = -1
                elif (next_board[i] == '0'):
                    two_dimensional_array[k][j] = 0
                i += 1
                j += 1
                if (i % 3 == 0):
                    j = 0
                    k += 1

            reshaped_data = two_dimensional_array.reshape(1, 3, 3, 1)
            score = model2.predict(reshaped_data)
            if score > max_score:
                max_score = score
                best_position = position

        self.buttons[best_position].text = 'O'
        self.update_board(best_position, "O")

        if self.check_winner("O"):
            self.show_message('OutMatched!', 'computer wins!')
        else:
            # Switch current player
            self.current_player = 'X'

    def play_best_position(self):
        available_positions = [i for i, char in enumerate(self.game_board) if char == "O"]

        best_position = None
        max_score = -1
        from_index = 0
        model3 = keras.models.load_model('saved model2.keras')
        two_dimensional_array = numpy.zeros((3, 3), int)
        for position in available_positions:
            nearby_places = self.available_positions_to(position)
            for pos in nearby_places:
                nex_board = self.game_board[:position] + "0" + self.game_board[position + 1:]
                next_board = nex_board[:pos] + "O" + nex_board[pos + 1:]

                k = 0
                j = 0
                i = 0

                while i < 9:
                    if (next_board[i] == 'X'):
                        two_dimensional_array[k][j] = 1
                    elif (next_board[i] == 'O'):
                        two_dimensional_array[k][j] = -1
                    elif (next_board[i] == '0'):
                        two_dimensional_array[k][j] = 0
                    i += 1
                    j += 1
                    if (i % 3 == 0):
                        j = 0
                        k += 1

                reshaped_data = two_dimensional_array.reshape(1, 3, 3, 1)
                score = model2.predict(reshaped_data)
                if score > max_score:
                    from_index = position
                    max_score = score
                    best_position = pos

        self.buttons[from_index].text = ''
        self.buttons[best_position].text = 'O'
        self.update_board(from_index, '0')
        self.update_board(best_position, "O")

        if self.check_winner("O"):
            self.show_message('OutMatched!', 'computer wins!')
        else:
            # Switch current player
            self.current_player = 'X'

    def available_positions_to(self, from_index):
        row = from_index // 3
        col = from_index % 3

        nearby_places = []

        for i in range(max(0, row - 1), min(3, row + 2)):
            for j in range(max(0, col - 1), min(3, col + 2)):
                nearby_index = i * 3 + j
                if self.is_valid_index(nearby_index) and self.buttons[nearby_index].text == '':
                    nearby_places.append(nearby_index)

        return nearby_places

    def is_valid_index(self, index):
        return 0 <= index < 9

    def check_winner(self, symbol):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]

        for combo in winning_combinations:
            if all(self.game_board[i] == symbol for i in combo):
                return True
        return False

    def update_board(self, index, symbol):
        self.game_board = self.game_board[:index] + symbol + self.game_board[index + 1:]
        self.game_board_history.append(self.game_board)

    def show_message(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200)).open()


class TMMApp(App):
    def build(self):
            self.instructionboard = InstructionBoard()
            self.instructionboard.TwoPlayers_button.bind(on_press=self.start_twoplayers)
            self.instructionboard.RandomCompute_button.bind(on_press=self.start_random)
            self.instructionboard.SmartComputer_button.bind(on_press=self.start_smart)
            self.instructionboard.NeuralSystem_button.bind(on_press=self.start_neural)
            return self.instructionboard

    def start_twoplayers(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(TwoPlayers())

    def start_random(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(RandomComputer())

    def start_smart(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(SmartComputer())

    def start_neural(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(NeuralSystem())

    #def on_start(self):
        # Open the window in full screen
        #Window.fullscreen = 'auto'


if __name__ == '__main__':
    TMMApp().run()