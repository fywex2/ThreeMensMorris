from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.app import App
import random
import numpy
import json


class ThreeMensMorrisBoard(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 3
        self.buttons = []
        self.all_pieces_placed = False
        self.selected_piece = None
        self.remaining_pieces = {'X': 3, 'O': 2}
        self.current_player = 'X'
        self.board = numpy.zeros((3, 3), int)
        self.game_board = "000000000"

        for i in range(9):
            button = Button(text='', font_size=24, size_hint=(None, None), width=200, height=200)
            button.bind(on_press=self.on_button_click)
            self.buttons.append(button)
            self.add_widget(button)

    def load_board_stats(self):
        global board_stats  # Use the global board_stats variable
        board_stats_file = "dict.json"
        try:
            with open(board_stats_file, 'r') as json_file:
                board_stats = json.load(json_file)

        except FileNotFoundError:
            board_stats = {}

    def on_button_click(self, button):
        row, col = self.buttons.index(button) // 3, self.buttons.index(button) % 3
        if not self.all_pieces_placed:
            # Placing phase
            #print(self.board)
            #print(self.remaining_pieces['O'])
            if button.text == '':
                if self.remaining_pieces[self.current_player] > 0:
                    button.text = self.current_player
                    self.remaining_pieces[self.current_player] -= 1

                    if self.current_player == 'X':
                        index = row * 3 + col
                        self.game_board = self.game_board[:index] + 'X' + self.game_board[index + 1:]
                        print(self.game_board)

                    # Check for winner after placing a piece
                    if self.check_winner():
                        winner = 'Player O' if self.current_player == 'O' else 'Player X'
                        self.show_message('Congratulations!', f'{winner} wins!')
                        return  # Stop further actions if there's a winner

                    self.current_player = 'O' if self.current_player == 'X' else 'X'



                    if all(self.remaining_pieces[player] == 0 for player in ['X', 'O']):
                        self.all_pieces_placed = True

                    if self.current_player == 'O':
                        # If it's computer's turn, make its move

                        self.computer_move()
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

                    if self.current_player == 'X':
                        index = row * 3 + col
                        self.game_board = self.game_board[:index] + 'X' + self.game_board[index + 1:]


                    if target_index in nearby_places:
                        # Move the piece to the target position
                        button.text = self.selected_piece.text
                        self.selected_piece.text = ''
                        self.game_board = self.game_board[:target_index] + '0' + self.game_board[target_index + 1:]
                        print(self.game_board)
                        self.selected_piece.background_color = (1, 1, 1, 1)  # Reset color
                        self.selected_piece = None

                        # Check for winner after moving a piece
                        if self.check_winner():
                            winner = 'Player O' if self.current_player == 'O' else 'Player X'
                            self.show_message('Congratulations!', f'{winner} wins!')
                        else:
                            # Switch current player
                            self.current_player = 'O' if self.current_player == 'X' else 'X'

                            if self.current_player == 'O':
                                # If it's computer's turn, make its move

                                self.computer_turn()

                    else:
                        self.show_message('Error', 'You can only move your piece to a nearby position.')

                else:
                    self.show_message('Error', 'You can only move your piece to an empty position.')

    def computer_move(self):
        empty_indices = [i for i, button in enumerate(self.buttons) if button.text == '']
        if empty_indices:
            # Choose a random empty spot for the computer's move
            index = random.choice(empty_indices)

            self.buttons[index].text = 'O'
            #self.game_board = self.game_board[:index] + 'O' + self.game_board[index + 1:]

            # Check for winner after computer's move
            if self.check_winner():
                winner = 'Player O' if self.current_player == 'O' else 'Player X'
                self.show_message('Congratulations!', f'{winner} wins!')
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

                if self.check_winner():
                    winner = 'Player O' if self.current_player == 'O' else 'Player X'
                    self.show_message('Congratulations!', f'{winner} wins!')
                else:
                    # Switch current player
                    self.current_player = 'X'

    def place_best_position(self):
        available_positions = [i for i, char in enumerate(self.game_board) if char == "0"]
        best_position = None
        max_score = -1

        for position in available_positions:
            next_board = self.game_board[:position] + "X" + self.game_board[position + 1:]
            if (next_board not in board_stats):
                score = 0
            else:
                (score,) = board_stats[next_board]
            if score > max_score:
                max_score = score
                best_position = position
        self.buttons[best_position].text = 'O'
        if self.check_winner():
            winner = 'Player O' if self.current_player == 'O' else 'Player X'
            self.show_message('Congratulations!', f'{winner} wins!')
        else:
            # Switch current player
            self.current_player = 'X'

    def play_best_position(self):
        available_positions = [i for i, char in enumerate(self.game_board) if char == "0"]

        best_position = None
        max_score = -1
        selected_piece = 0

        if available_positions:
            for position in available_positions:
                nearby_places = self.available_positions_to(position)
                for pos in nearby_places:
                    next_board = self.game_board[:position] + "0" + self.game_board[position + 1:]
                    next_board = self.game_board[:pos] + "X" + self.game_board[pos + 1:]
                    if (next_board not in board_stats):
                        score = 0
                    else:
                        (score,) = board_stats[next_board]
                    if score > max_score:
                        selected_piece = position
                        max_score = score
                        best_position = pos

            self.buttons[best_position].text = selected_piece.text
            selected_piece.text = ''

            # Reset color (assuming you change the color when a piece is selected)
            selected_piece.background_color = (1, 1, 1, 1)  # Reset color

            if self.check_winner():
                winner = 'Player O' if self.current_player == 'O' else 'Player X'
                self.show_message('Congratulations!', f'{winner} wins!')
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

    def check_winner(self):
        symbol = self.current_player

        winning_combinations = [
            (0, 1, 2),  # Top row
            (3, 4, 5),  # Middle row
            (6, 7, 8),  # Bottom row
            (0, 3, 6),  # Left column
            (1, 4, 7),  # Middle column
            (2, 5, 8),  # Right column
            (0, 4, 8),  # Diagonal from top-left to bottom-right
            (2, 4, 6)  # Diagonal from top-right to bottom-left
        ]
        for combination in winning_combinations:
            if all(self.buttons[i].text == symbol for i in combination):
                return True  # Found a winning combination

        return False  # No winning combination found

    def show_message(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200)).open()


class ThreeMensMorrisApp(App):
    def build(self):
        board = ThreeMensMorrisBoard()

        # Set the size of the window to 600x600 pixels
        Window.size = (600, 600)

        # Return the root widget
        return board


if __name__ == "__main__":
    ThreeMensMorrisApp().run()