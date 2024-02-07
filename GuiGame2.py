# Import Kivy modules
import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line, Color

# Define the board widget
class Board(Widget):
    # Initialize the board
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        # Draw the grid lines
        with self.canvas:
            Color(0, 0, 0)
            Line(points=[self.center_x - 100, self.center_y - 100, self.center_x + 100, self.center_y - 100])
            Line(points=[self.center_x - 100, self.center_y, self.center_x + 100, self.center_y])
            Line(points=[self.center_x - 100, self.center_y + 100, self.center_x + 100, self.center_y + 100])
            Line(points=[self.center_x - 100, self.center_y - 100, self.center_x - 100, self.center_y + 100])
            Line(points=[self.center_x, self.center_y - 100, self.center_x, self.center_y + 100])
            Line(points=[self.center_x + 100, self.center_y - 100, self.center_x + 100, self.center_y + 100])
        # Create a list of buttons for the board cells
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = Button(text="", font_size=50, background_color=(1, 1, 1, 1))
                button.bind(on_press=self.on_button_press)
                button.pos = (self.center_x - 150 + i * 100, self.center_y - 150 + j * 100)
                button.size = (100, 100)
                self.add_widget(button)
                self.buttons.append(button)
        # Set the initial game state
        self.turn = "X" # X goes first
        self.phase = "place" # First phase is placing pieces
        self.pieces = {"X": 0, "O": 0} # Number of pieces placed by each player
        self.winner = None # No winner yet

    # Handle button press events
    def on_button_press(self, button):
        # Check if the game is over
        if self.winner is not None:
            return
        # Check if the button is empty
        if button.text == "":
            # Check if the phase is placing
            if self.phase == "place":
                # Place the piece of the current player
                button.text = self.turn
                # Increase the number of pieces placed by the current player
                self.pieces[self.turn] += 1
                # Check if the current player has formed a line of three
                if self.check_win(self.turn):
                    # Declare the winner
                    self.winner = self.turn
                    self.parent.ids.message.text = f"{self.turn} wins!"
                # Check if both players have placed all their pieces
                elif self.pieces["X"] == 3 and self.pieces["O"] == 3:
                    # Switch to the moving phase
                    self.phase = "move"
                    self.parent.ids.message.text = f"{self.turn}'s turn to move"
                # Otherwise, switch to the next player
                else:
                    self.switch_turn()
            # Check if the phase is moving
            elif self.phase == "move":
                # Select the piece of the current player to move
                self.selected = button
                self.selected.background_color = (0.5, 0.5, 0.5, 1)
                # Change the phase to moving
                self.phase = "moving"
        # Check if the button is not empty
        else:
            # Check if the phase is moving
            if self.phase == "moving":
                # Check if the button is adjacent to the selected piece
                if self.is_adjacent(self.selected, button):
                    # Move the piece of the current player
                    button.text = self.selected.text
                    self.selected.text = ""
                    self.selected.background_color = (1, 1, 1, 1)
                    # Check if the current player has formed a line of three
                    if self.check_win(self.turn):
                        # Declare the winner
                        self.winner = self.turn
                        self.parent.ids.message.text = f"{self.turn} wins!"
                    # Otherwise, switch to the next player
                    else:
                        self.switch_turn()
                # Deselect the piece
                self.selected.background_color = (1, 1, 1, 1)
                # Change the phase to move
                self.phase = "move"

    # Switch to the next player
    def switch_turn(self):
        # Toggle between X and O
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
        # Update the message
        self.parent.ids.message.text = f"{self.turn}'s turn to {self.phase}"

    # Check if a player has formed a line of three
    def check_win(self, player):
        # Check the rows
        for i in range(0, 9, 3):
            if self.buttons[i].text == self.buttons[i + 1].text == self.buttons[i + 2].text == player:
                return True
        # Check the columns
        for i in range(3):
            if self.buttons[i].text == self.buttons[i + 3].text == self.buttons[i + 6].text == player:
                return True
        # Check the diagonals
        if self.buttons[0].text == self.buttons[4].text == self.buttons[8].text == player:
            return True
        if self.buttons[2].text == self.buttons[4].text == self.buttons[6].text == player:
            return True
        # No line of three
        return False

    # Check if two buttons are adjacent on the grid
    def is_adjacent(self, button1, button2):
        # Get the indices of the buttons
        i1 = self.buttons.index(button1)
        i2 = self.buttons.index(button2)
        # Get the row and column of the buttons
        r1 = i1 // 3
        c1 = i1 % 3
        r2 = i2 // 3
        c2 = i2 % 3
        # Check if the row or column difference is one
        return abs(r1 - r2) + abs(c1 - c2) == 1

# Define the main app class
class ThreeMensMorrisApp(App):
    # Build the app
    def build(self):
        # Create a box layout for the main window
        layout = BoxLayout(orientation="vertical")
        # Create a label for the message
        message = Label(text="X's turn to place", font_size=30)
        # Create a custom property for the label id
        message.label_id = ObjectProperty("message")
        # Create a board widget
        board = Board()
        # Add the widgets to the layout
        layout.add_widget(message)
        layout.add_widget(board)
        # Return the layout
        return layout


# Run the app
if __name__ == "__main__":
    ThreeMensMorrisApp().run()