from random import randint, shuffle


def print_board(board):
    """
    Prints the sudoku board with proper formatting.
    """
    for i in range(9):
        if i % 3 == 0 and i != 0:  # Add a horizontal separator every 3 rows
            print("-" * 25)

        row = ""
        for j in range(9):
            if j % 3 == 0 and j != 0:  # Add a vertical separator every 3 columns
                row += "| "
            row += f"{board[i][j] if board[i][j] != 0 else '.'} "
        print(row)


def find_empty(board):
    """
    Finds the next empty cell in the sudoku board.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def valid(board, pos, num):
    """
    Checks if a number is valid at a given position.
    """
    if num < 1 or num > 9:
        return False

    for i in range(9):
        if board[i][pos[1]] == num or board[pos[0]][i] == num:
            return False

    start_i = pos[0] - pos[0] % 3
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):
            if board[start_i + i][start_j + j] == num:
                return False

    return True


def solve(board):
    """
    Solves the sudoku board using backtracking.
    """
    empty = find_empty(board)
    if not empty:
        return True

    for num in range(1, 10):
        if valid(board, empty, num):
            board[empty[0]][empty[1]] = num

            if solve(board):
                return True

            board[empty[0]][empty[1]] = 0  # Backtrack

    return False


def generate_board():
    """
    Generates a random sudoku board with a unique solution.
    """
    board = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()

    def fill_cells(board):
        empty = find_empty(board)
        if not empty:
            return True

        nums = list(range(1, 10))
        shuffle(nums)
        for num in nums:
            if valid(board, empty, num):
                board[empty[0]][empty[1]] = num

                if fill_cells(board):
                    return True

                board[empty[0]][empty[1]] = 0  # Backtrack
        return False

    fill_cells(board)

    removed_cells = set()
    while len(removed_cells) < randint(55, 65):
        row, col = randint(0, 8), randint(0, 8)
        if (row, col) not in removed_cells:
            removed_cells.add((row, col))
            backup = board[row][col]
            board[row][col] = 0

            temp_board = [row[:] for row in board]
            if not solve(temp_board):
                board[row][col] = backup

    return board


if __name__ == "__main__":
    board = generate_board()
    print("Generated Board:")
    print_board(board)
    solve(board)
    print("***** Solved Board *****")
    print_board(board)

