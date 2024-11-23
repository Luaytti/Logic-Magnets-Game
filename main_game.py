import tkinter as tk
from tkinter import messagebox, ttk
from algorithms import solve_with_bfs, solve_with_dfs, solve_with_ucs, solve_with_hill_climbing

class State:
    def __init__(self, board_size, init_board):
        self.board_size = board_size
        self.board = init_board
        self.original_board = [row[:] for row in init_board]
        self.selected_piece = None

    def reset(self):
        self.board = [row[:] for row in self.original_board]
        self.selected_piece = None

    def is_winner(self):
        for row in self.board:
            for cell in row:
                if cell == 'E':
                    return False
        return True

    def move_piece(self, current_row, current_col, new_row, new_col):
        piece = self.board[current_row][current_col]
        if piece == 'P':
            return self.repulsion(current_row, current_col, new_row, new_col)
        elif piece == 'R':
            return self.attraction(current_row, current_col, new_row, new_col)
        return False

    def repulsion(self, current_row, current_col, next_row, next_col):
        if not self.valid_move(next_row, next_col):
            return False
        self.board[current_row][current_col] = 'E'
        self.board[next_row][next_col] = 'P'
        return True

    def attraction(self, current_row, current_col, next_row, next_col):
        if not self.valid_move(next_row, next_col):
            return False
        self.board[current_row][current_col] = 'E'
        self.board[next_row][next_col] = 'R'
        return True

    def valid_move(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == 'E'

class LogicMagnetsGame:
    def __init__(self, root, state):
        self.root = root
        self.state = state
        self.mode = 'user'
        self.selected_piece = None
        self.root.title("Logic Magnets")
        self.grid_buttons = []
        self.create_controls()
        self.create_grid()
        self.update_grid()

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=0, padx=10, pady=10)
        tk.Label(control_frame, text="Mode:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        mode_dropdown = ttk.Combobox(control_frame, values=["user", "solver"], state="readonly")
        mode_dropdown.set(self.mode)
        mode_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        mode_dropdown.bind("<<ComboboxSelected>>", self.set_mode)
        tk.Label(control_frame, text="Algorithm:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.algo_dropdown = ttk.Combobox(control_frame, values=["BFS", "DFS", "UCS", "Hill Climbing"], state="readonly")
        self.algo_dropdown.set("BFS")
        self.algo_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        tk.Button(control_frame, text="Solve", command=self.solve_game).grid(row=1, column=0, columnspan=4, pady=5)

    def create_grid(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=1, column=0, padx=10, pady=10)
        for row in range(self.state.board_size):
            button_row = []
            for col in range(self.state.board_size):
                button = tk.Button(self.grid_frame, width=6, height=3, command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.grid_buttons.append(button_row)

    def set_mode(self, event):
        self.mode = event.widget.get()
        self.selected_piece = None

    def solve_game(self):
        if self.mode == 'solver':
            algorithm = self.algo_dropdown.get()
            moves = []
            if algorithm == "BFS":
                moves = solve_with_bfs(self.state.board)
            elif algorithm == "DFS":
                moves = solve_with_dfs(self.state.board)
            elif algorithm == "UCS":
                moves = solve_with_ucs(self.state.board)
            elif algorithm == "Hill Climbing":
                moves = solve_with_hill_climbing(self.state.board)

            if moves:
                self.show_solution(moves)
            else:
                messagebox.showinfo("No Solution", "No solution found.")
        else:
            messagebox.showinfo("Invalid Mode", "Switch to solver mode to solve the puzzle.")

    def show_solution(self, moves):
        for move in moves:
            row, col = move
            self.state.move_piece(self.selected_piece[0], self.selected_piece[1], row, col)
            self.update_grid()

    def on_button_click(self, row, col):
        if self.mode == 'user':
            self.user_move(row, col)

    def user_move(self, row, col):
        if self.selected_piece:
            current_row, current_col = self.selected_piece
            if self.state.move_piece(current_row, current_col, row, col):
                self.update_grid()
                self.selected_piece = None
                if self.state.is_winner():
                    messagebox.showinfo("You Win!", "Congratulations! You've solved the puzzle.")
            else:
                messagebox.showerror("Invalid Move", "This move is not valid.")
        else:
            piece = self.state.board[row][col]
            if piece in ('P', 'R', 'G'):
                self.selected_piece = (row, col)

    def update_grid(self):
        for row in range(self.state.board_size):
            for col in range(self.state.board_size):
                piece = self.state.board[row][col]
                color = self.get_piece_color(piece)
                self.grid_buttons[row][col].config(bg=color, text=piece)

    def get_piece_color(self, piece):
        if piece == 'P':
            return 'purple'
        elif piece == 'R':
            return 'red'
        elif piece == 'G':
            return 'gray'
        elif piece == '*':
            return 'white'
        elif piece == 'E':
            return 'light blue'
        else:
            return 'white'

def main():
    board_size = 5
    init_board = [
        ['*', 'G', '*', 'G', '*'],
        ['E', 'E', 'P', 'E', 'E'],
        ['E', 'E', 'E', 'E', 'E'],
        ['E', 'E', 'E', 'E', 'E'],
        ['E', 'E', 'E', 'E', 'E']
    ]
    state = State(board_size, init_board)
    root = tk.Tk()
    game = LogicMagnetsGame(root, state)
    root.mainloop()

if __name__ == "__main__":
    main()
