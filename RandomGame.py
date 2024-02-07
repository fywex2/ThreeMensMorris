# importing needed packages

import itertools
import random
from collections import defaultdict
import numpy as np
import json
import copy

# storing the dictionary in a variable
with open("dict.json", 'r') as fp:
    existing_data = json.load(fp)
with open("dict2.json", 'r') as fp:
    existing_data2 = json.load(fp)

# saving all the boards in the game and their scores
states = []
states_scores = []

# flattening the list to a string
def flatten_list(list):
    flat_list = []
    for row in list:
        flat_list.extend(row)
    return "".join(str(element) for element in flat_list)

# we will play the game of three men's morris as an agent (2), the opponent will be (1)
class ThreeMensMorris:

    def __init__(self):
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]  # the board of the game, 0 is an empty space
        self.won = 0  # who won the game
        self.gama = 0.9  # he called discorent how much down we want to get between board (0.9 to 1)
        self.num_agent_pieces = 3
        self.num_opp_pieces = 3
        self.phase2_close = {  # all the possible moves for each position in the second phase of the game
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
        self.num_moves = 0  # number of moves that have been made in the game
        self.starts_first = random.choice([1, 2])  # choosing who will start the game 1 or 2

    # returns a list of the legal places in the first phase of the game in the board
    def legal_phase1(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == 0]

    # returning a list of the legal places to move to in the second phase of the game
    def legal_phase2(self, position):
        row, col = position
        legal = self.phase2_close[row, col]
        return [(row, col) for (row, col) in legal if self.board[row][col] == 0]

    # where are the agent pieces on the board
    def agent_pieces(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == 2]

    # where are the opponent pieces on the board
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

    # the turn of the agent in the game
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

    # the turn of the opponent in the game
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

    # smart agent turn using the dictionary and the board scores
    def smart_agent_turn(self):
        max_score = -1
        max_location = ((0, 0), (0, 0))

        if self.num_agent_pieces > 0:
            for i, j in itertools.product(range(3), range(3)):
                if self.board[i][j] == 0:
                    temp_board = copy.deepcopy(self.board)
                    temp_board[i][j] = 2
                    str_board = flatten_list(temp_board)

                    if max_score < existing_data[str_board][0]:
                        max_score = existing_data[str_board][0]
                        max_location = ((i, j), (0, 0))
            self.num_agent_pieces -= 1

            self.board[max_location[0][0]][max_location[0][1]] = 2

        else:
            for i, j in itertools.product(range(3), range(3)):
                if self.board[i][j] == 2:
                    for c in range(len(self.phase2_close[i, j])):
                        temp_board = copy.deepcopy(self.board)
                        row, col = self.phase2_close[i, j][c]
                        if self.board[row][col] == 0:
                            temp_board[i][j] = 0
                            temp_board[row][col] = 2
                            str_board = flatten_list(temp_board)
                            if max_score < existing_data[str_board][0]:
                                max_score = existing_data[str_board][0]
                                max_location = ((i, j), (row, col))
            self.board[max_location[0][0]][max_location[0][1]] = 0
            self.board[max_location[1][0]][max_location[1][1]] = 2

    # smart opp turn using the dictionary and the board scores
    def smart_opp_turn(self):
        max_score = -1
        max_location = ((0, 0), (0, 0))

        if self.num_agent_pieces > 0:
            for i, j in itertools.product(range(3), range(3)):
                if self.board[i][j] == 0:
                    temp_board = copy.deepcopy(self.board)
                    temp_board[i][j] = 1
                    str_board = flatten_list(temp_board)

                    if max_score < existing_data2[str_board][0]:
                        max_score = existing_data2[str_board][0]
                        max_location = ((i, j), (0, 0))
            self.num_agent_pieces -= 1

            self.board[max_location[0][0]][max_location[0][1]] = 1

        else:
            for i, j in itertools.product(range(3), range(3)):
                if self.board[i][j] == 1:
                    for c in range(len(self.phase2_close[i, j])):
                        temp_board = copy.deepcopy(self.board)
                        row, col = self.phase2_close[i, j][c]
                        if self.board[row][col] == 0:
                            temp_board[i][j] = 0
                            temp_board[row][col] = 1
                            str_board = flatten_list(temp_board)
                            if max_score < existing_data2[str_board][0]:
                                max_score = existing_data2[str_board][0]
                                max_location = ((i, j), (row, col))
            self.board[max_location[0][0]][max_location[0][1]] = 0
            self.board[max_location[1][0]][max_location[1][1]] = 1

    # ranking all the boards in the game and storing them
    def rank_board_state(self):
        rank = self.gama ** self.num_moves
        if self.starts_first == 2:
            if self.is_win() == 1:
                rank = 0
            if self.is_win() == 2:
                rank = 1

        else:
            if self.is_win() == 1:
                rank = 1
            if self.is_win() == 2:
                rank = 0

        states.append(flatten_list(self.board))
        rank = float(rank)
        states_scores.append(rank)

# class that manages the game
class Games:

    def __init__(self):
        self.agent_win_amount = 0  # amount of agent wins
        self.opp_win_amount = 0  # amount of opp wins
        self.amount_games = 10000  # amount of games to run
        self.tmm = ThreeMensMorris()  # the variable of the game

    # run a single game
    def play_game(self):
        turn = self.tmm.starts_first
        if self.tmm.starts_first == 1:
            while self.tmm.is_win() == 0:
                if turn == 1:
                    self.tmm.smart_opp_turn()
                    turn = 2
                else:
                    self.tmm.agent_turn()
                    turn = 1
                print(self.tmm.board)
        else:
            while self.tmm.is_win() == 0:
                if turn == 1:
                    self.tmm.opp_turn()
                    turn = 2
                else:
                    self.tmm.smart_agent_turn()
                    turn = 1
                print(self.tmm.board)

    # run multiply games
    def multiply_games(self):
        aggregated_dict = defaultdict(lambda: {'total_rank': 0, 'count': 0})

        for _ in range(self.amount_games):
            if _ % 1 == 0:
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


games = Games()  # creating a variable of running the games

dict_result = games.multiply_games()  # running multiply games and saving it to the dictionary

#with open("dict2.json", "w") as fp:  # saving the final dictionary to the json file
#   json.dump(dict_result, fp)

print(f"agent wins:{games.agent_win_amount}")  # displaying the amount of wins for agent
print(f"opponent wins:{games.opp_win_amount}")  # displaying the amount of wins for opponent
