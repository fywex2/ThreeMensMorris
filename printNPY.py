def check_block(prev_board, board):
    # Define winning combinations
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)],  # Row 1
        [(1, 0), (1, 1), (1, 2)],  # Row 2
        [(2, 0), (2, 1), (2, 2)],  # Row 3
        [(0, 0), (1, 0), (2, 0)],  # Column 1
        [(0, 1), (1, 1), (2, 1)],  # Column 2
        [(0, 2), (1, 2), (2, 2)],  # Column 3
        [(0, 0), (1, 1), (2, 2)],  # Diagonal \
        [(0, 2), (1, 1), (2, 0)]  # Diagonal /
    ]

    for combination in winning_combinations:
        x_count = 0
        empty_spot = None
        for cell in combination:
            if prev_board[cell[0]][cell[1]] == 2:
                x_count += 1
            elif prev_board[cell[0]][cell[1]] == 0:
                empty_spot = cell

        # If there are two X's and one empty spot in a combination
        if x_count == 2 and empty_spot and prev_board[empty_spot[0]][empty_spot[1]] == 0:
            # Check if O blocked the empty spot
            if board[empty_spot[0]][empty_spot[1]] == 1:
                return True  # Block found, return True

    return False  # No block found in any combination

# Another example with a block:
prev_board = [[2, 1, 0],
              [0, 2, 0],
              [0, 0, 0]]
current_board = [[2, 1, 0],
                 [0, 2, 0],
                 [0, 0, 1]]  # Block! 'O' fills the empty spot in a winning combination

if check_block(prev_board, current_board):
    print("There is a block made by O to prevent X from winning.")
else:
    print("No block found.")
