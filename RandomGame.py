import itertools
import random
from collections import defaultdict
import numpy as np
import json
import copy

with open("dict.json", 'r') as fp:
    existing_data = json.load(fp)
states = []
states_scores = []

def flatten_list(list):
    flat_list = []
    for row in list:
        flat_list.extend(row)
    return "".join(str(element) for element in flat_list)

class ThreeMensMorris:
    # we will play as an agent (2), the opponnent will be (1)

    def __init__(self):
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.won = 0
        self.win_points_agent = 1  # it is recommended to give 1 or 10
        self.loss_points_agent = 0
        self.all_boards_in_game = []  # only number sting
        self.gama = 0.9  # he called discorent how much down we want to get between board (0.9 to 1)
        self.num_agent_pieces = 3
        self.num_opp_pieces = 3
        self.phase2_close = {
            (0, 0): [(0, 1), (1, 0), (1, 1)],
            (0, 1): [(0, 0), (0, 2), (1, 1)],
            (0, 2): [(1, 1), (1, 2), (0, 1)],
            (1, 0): [(0, 0), (2, 0), (1, 1)],
            (1, 1): [(i, j) for i in range(3) for j in range(3) if (i, j) != (1, 1)],
            (1, 2): [(0, 2), (2, 2), (1, 1)],
            (2, 0): [(1, 1), (1, 0), (2, 1)],
            (2, 1): [(1, 1), (2, 0), (2, 2)],
            (2, 2): [(1, 1), (1, 2), (2, 1)]
        }
        self.num_moves = 0

    # returns a list of the legal places in the board (as tupples)
    def legal_phase1(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == 0]

    def legal_phase2(self, position):
        # Define neighboring positions
        row, col = position
        legal = self.phase2_close[row, col]
        return [(row, col) for (row, col) in legal if self.board[row][col] == 0]

    def agent_pieces(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == 2]

    def opp_pieces(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == 1]

    # checks for wins in all rows, columns, and diagonals of the 5x5 board
    def is_win(self):
        # Check rows and columns for a line
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] in [1, 2]:
                return self.board[i][0]
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] in [1, 2]:
                return self.board[0][i]

        # Check diagonals for a line
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] in [1, 2]:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] in [1, 2]:
            return self.board[0][2]

        return 0  # No winner yet

    def agent_turn(self):
        if self.num_agent_pieces > 0:
            row, col = random.choice(self.legal_phase1())
            self.board[row][col] = 2
            self.num_agent_pieces -= 1

        else:
            row1, col1 = random.choice(self.agent_pieces())
            while len(self.legal_phase2([row1, col1])) == 0:
                row1, col1 = random.choice(self.agent_pieces())
            self.board[row1][col1] = 0
            row2, col2 = random.choice(self.legal_phase2([row1, col1]))
            self.board[row2][col2] = 2

        self.rank_board_state()
        self.num_moves += 1

    def opp_turn(self):
        if self.num_opp_pieces > 0:
            row, col = random.choice(self.legal_phase1())
            self.board[row][col] = 1
            self.num_opp_pieces -= 1

        else:
            row1, col1 = random.choice(self.opp_pieces())
            while len(self.legal_phase2([row1, col1])) == 0:
                row1, col1 = random.choice(self.opp_pieces())
            self.board[row1][col1] = 0
            row2, col2 = random.choice(self.legal_phase2([row1, col1]))
            self.board[row2][col2] = 1

        self.rank_board_state()
        self.num_moves += 1


    def smart_agent_turn(self):
        max_score = -1
        max_location = (0, 0)

        for i, j in itertools.product(range(3), range(3)):
            if self.board[i][j] == 0:
                temp_board = self.board
                temp_board[i][j] = 2


        self.board[max_location[0]][max_location[1]] = 2

    # manages the game from start to finish

    # the def will give points to every board in this game
    # every list will have 2 cell of the board and the points the board got in the game
    def rank_board_state(self):
        rank = self.gama ** self.num_moves
        if self.is_win() == 1:
            rank = self.loss_points_agent
        if self.is_win() == 2:
            rank = self.win_points_agent

        rank = float(rank)
        states.append(flatten_3x3_list(self.board))
        states_scores.append(rank)

class Games:
    def __init__(self):
        self.agent_win_amount = 0
        self.opp_win_amount = 0
        self.amount_games = 1000000
        self.tmm = ThreeMensMorris()

    def play_game(self):
        turn = 2
        while self.tmm.is_win() == 0:
            if turn == 1:
                self.tmm.opp_turn()
                turn = 2
            else:
                self.tmm.agent_turn()
                turn = 1

    def multiply_games(self):
        aggregated_dict = defaultdict(lambda: {'total_rank': 0, 'count': 0})

        for _ in range(self.amount_games):
            if _ % 10000 == 0:
                print(_)
            self.tmm = ThreeMensMorris()
            self.play_game()
            won = self.tmm.is_win()
            if won == 1:
                self.opp_win_amount += 1
            elif won == 2:
                self.agent_win_amount += 1

        for board, rank in zip(states, states_scores):
            aggregated_dict[board]['total_rank'] += rank
            aggregated_dict[board]['count'] += 1

        return {
            **existing_data,
            **{
                board: [data['total_rank'] / data['count'], data['count']]
                for board, data in aggregated_dict.items()
            },
        }

games = Games()

dict_result = games.multiply_games()
final_dict = dict(existing_data, **dict_result)
with open("dict.json", "w") as fp:
    json.dump(final_dict, fp)

print(f"agent wins:{games.agent_win_amount}")
print(f"opponent wins:{games.opp_win_amount}")
