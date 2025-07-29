#Task 6: More on Classes

class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class Board:
    valid_moves = [
        "upper left", "upper center", "upper right",
        "middle left", "center", "middle right",
        "lower left", "lower center", "lower right"
    ]

    def __init__(self):
        self.board_array = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        self.last_move = None

    def __str__(self):
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)

    def move(self, move_string):
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
        self.board_array[row][column] = self.turn
        self.last_move = move_string
        self.turn = "O" if self.turn == "X" else "X"

    def whats_next(self):
        cat = True
        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
        if cat:
            return (True, "Cat's Game.")
        
        win = False
        for i in range(3):  # rows
            if self.board_array[i][0] != " " and self.board_array[i][0] == self.board_array[i][1] == self.board_array[i][2]:
                win = True
        for i in range(3):  # columns
            if self.board_array[0][i] != " " and self.board_array[0][i] == self.board_array[1][i] == self.board_array[2][i]:
                win = True
        if self.board_array[1][1] != " ":  # diagonals
            if self.board_array[0][0] == self.board_array[1][1] == self.board_array[2][2]:
                win = True
            if self.board_array[0][2] == self.board_array[1][1] == self.board_array[2][0]:
                win = True

        if win:
            winner = "O" if self.turn == "X" else "X"
            return (True, f"{winner} wins!")
        else:
            return (False, f"{self.turn}'s turn.")

if __name__ == "__main__":
    board = Board()
    print("Welcome to Tic Tac Toe!\n")
    print("Valid moves are:", ", ".join(Board.valid_moves))
    print()

    while True:
        print(board)
        print()
        status, message = board.whats_next()
        if status:
            print(message)
            break

        move = input(f"{board.turn}'s move (type the position): ").strip().lower()
        try:
            board.move(move)
        except TictactoeException as e:
            print(f"Error: {e.message}") 