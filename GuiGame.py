from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class ThreeMensMorrisBoard(GridLayout):
    def __init__(self, **kwargs):
        super(ThreeMensMorrisBoard, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 4
        self.board_state = [''] * 9
        self.player_turn = 'X'
        self.pieces_placed = {'X': 0, 'O': 0}
        self.selected_piece_index = None

        for i in range(9):
            button = Button(text='', font_size=40, on_press=self.on_button_click)
            button.index = i  # Set the index attribute for each button
            self.add_widget(button)

        self.status_label = Label(text=f"Player {self.player_turn}'s turn - Placing", font_size=20)
        self.add_widget(self.status_label)

    def place_piece(self, instance, index):
        self.board_state[index] = self.player_turn
        instance.text = self.player_turn
        self.pieces_placed[self.player_turn] += 1
        self.check_phase_transition()

    def move_piece(self, instance, index):
        if self.selected_piece_index is not None:
            # Player has selected a piece, move it to the selected destination
            if self.board_state[index] == '':
                self.board_state[self.selected_piece_index] = ''
                self.board_state[index] = self.player_turn
                self.children[self.selected_piece_index].text = ''
                instance.text = self.player_turn
                self.selected_piece_index = None
                self.moves_counter = 1
                self.status_label.text = f"Player {self.player_turn}'s turn - Placing"
            else:
                # The destination is occupied, stay in the moving phase
                self.status_label.text = f"Player {self.player_turn}'s turn - Moving (Choose a valid destination)"
                self.selected_piece_index = None

    def on_button_click(self, instance):
        index = instance.index  # Retrieve the index attribute from the button
        print(f"Clicked button index: {index}")

        if self.board_state[index] == '':
            print(f"Current player turn: {self.player_turn}")
            if self.pieces_placed[self.player_turn] < 3:
                # Placing mode
                self.place_piece(instance, index)
            else:
                # Moving mode
                self.move_piece(instance, index)

            if self.check_winner():
                self.status_label.text = f"Player {self.player_turn} wins!"
            else:
                self.switch_player_turn()

    def switch_player_turn(self):
        self.player_turn = 'O' if self.player_turn == 'X' else 'X'

    def check_winner(self):
        for i in range(3):
            if (
                self.board_state[i] == self.board_state[i + 3] == self.board_state[i + 6] == self.player_turn
                or self.board_state[i * 3] == self.board_state[i * 3 + 1] == self.board_state[i * 3 + 2] == self.player_turn
            ):
                return True

        if (
            self.board_state[0] == self.board_state[4] == self.board_state[8] == self.player_turn
            or self.board_state[2] == self.board_state[4] == self.board_state[6] == self.player_turn
        ):
            return True

        return False

    def check_phase_transition(self):
        if self.pieces_placed[self.player_turn] == 3:
            self.status_label.text = f"Player {self.player_turn}'s turn - Moving"
            self.selected_piece_index = None  # Reset selected piece index for the moving phase


class ThreeMensMorrisApp(App):
    def build(self):
        return ThreeMensMorrisBoard()


if __name__ == '__main__':
    ThreeMensMorrisApp().run()
