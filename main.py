from tkinter import *
from tkinter import ttk
import numpy as np
import random


# ## For future update:
# Add 3 buttons
# Window size = FHD
# Add button for restart
# option for timer


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title('Tic-Tac-Toe')
        self.root.bind('<Button-1>', self.click)  # user input
        self.root.bind('<Button-3>', self.click_reset_mouse)  # user input

        self.list_number_of_players = [2, 2, 3, 4, 5]
        self.list_board_matrix = [3, 3, 4, 5, 6, 7, 8, 9, 10]
        self.list_symbols_in_series = [3, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.green_color = '#7BC043'
        self.generic_color = 'gray'

        self.number_of_players_gui = IntVar(value=self.list_number_of_players[0])
        self.board_matrix_x = IntVar(value=self.list_board_matrix[0])
        self.board_matrix_y = IntVar(value=self.list_board_matrix[0])
        self.symbols_for_win_x = IntVar(value=self.list_symbols_in_series[0])
        self.symbols_for_win_y = IntVar(value=self.list_symbols_in_series[0])
        self.symbols_for_win_z = IntVar(value=self.list_symbols_in_series[0])

        self.canvas = Canvas()
        self.game_status = 0

        self.number_of_players = None
        self.board_matrix = None
        self.symbols_for_win = None
        self.size_of_box = None
        self.symbol_size = None
        self.symbol_thickness = None
        self.symbol_colors = None
        self.player_turn = None
        self.board_status = None
        self.starting_player = None
        self.tie = None
        self.tie_score = None
        self.player_wins = None
        self.player_scores = None
        self.last_winner = None
        self.label_players = None
        self.dropdown_players = None
        self.label_board_size = None
        self.dropdown_board_size_x = None
        self.dropdown_board_size_y = None
        self.label_symbols_for_win = None
        self.dropdown_symbols_for_win_x = None
        self.dropdown_symbols_for_win_y = None
        self.dropdown_symbols_for_win_z = None
        self.button_submit = None
        self.button_reset = None
        self.button_reset2 = None
        self.button_reset3 = None
        self.show_welcome_canvas()

    def show_welcome_canvas(self):
        style = ttk.Style()
        style.configure('my.TMenubutton', font=('Helvetica', 15))
        style.configure('my.TButton', font=('Helvetica', 15))
        pad_x = 15
        pad_y = 15
        self.label_players = ttk.Label(self.root, text="Number of Players:", font=15)
        self.label_players.grid(row=0, column=0, padx=pad_x, pady=pad_y, sticky=W)
        self.dropdown_players = ttk.OptionMenu(self.root, self.number_of_players_gui, *self.list_number_of_players, style='my.TMenubutton')
        self.dropdown_players.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky=W)

        self.label_board_size = ttk.Label(self.root, text="Board Size (x, y):", font=15)
        self.label_board_size.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky=W)
        self.dropdown_board_size_x = ttk.OptionMenu(self.root, self.board_matrix_x, *self.list_board_matrix, style='my.TMenubutton')
        self.dropdown_board_size_x.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)
        self.dropdown_board_size_y = ttk.OptionMenu(self.root, self.board_matrix_y, *self.list_board_matrix, style='my.TMenubutton')
        self.dropdown_board_size_y.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky=W)

        self.label_symbols_for_win = ttk.Label(self.root, text="Symbols in Series (x, y, z):", font=15)
        self.label_symbols_for_win.grid(row=2, column=0, padx=pad_x, pady=pad_y, sticky=W)
        self.dropdown_symbols_for_win_x = ttk.OptionMenu(self.root, self.symbols_for_win_x, *self.list_symbols_in_series, style='my.TMenubutton')
        self.dropdown_symbols_for_win_x.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky=W)
        self.dropdown_symbols_for_win_y = ttk.OptionMenu(self.root, self.symbols_for_win_y, *self.list_symbols_in_series, style='my.TMenubutton')
        self.dropdown_symbols_for_win_y.grid(row=2, column=2, padx=pad_x, pady=pad_y, sticky=W)
        self.dropdown_symbols_for_win_z = ttk.OptionMenu(self.root, self.symbols_for_win_z, *self.list_symbols_in_series, style='my.TMenubutton')
        self.dropdown_symbols_for_win_z.grid(row=2, column=3, padx=pad_x, pady=pad_y, sticky=W)

        self.button_submit = ttk.Button(self.root, text="Submit", command=self.get_selected_values, style='my.TButton')
        self.button_submit.grid(row=3, column=0, columnspan=4, pady=50, sticky=S)

    def get_selected_values(self):
        self.number_of_players = self.number_of_players_gui.get()
        self.board_matrix = (self.board_matrix_x.get(), self.board_matrix_y.get())
        self.symbols_for_win = (self.symbols_for_win_x.get(), self.symbols_for_win_y.get(), self.symbols_for_win_z.get())
        self.size_of_box = 250 - int(sum(self.board_matrix) / 2) * 18
        self.symbol_size = (self.size_of_box - self.size_of_box / 3) / 2
        self.symbol_thickness = (self.size_of_box - self.size_of_box / 3) / 3
        self.symbol_colors = ['#{:06x}'.format(random.randint(0x111111, 0xEEEEEE)) for _ in range(self.number_of_players)]  # 0 and F are too extreme

        self.label_players.grid_remove()
        self.dropdown_players.grid_remove()
        self.label_board_size.grid_remove()
        self.dropdown_board_size_x.grid_remove()
        self.dropdown_board_size_y.grid_remove()
        self.label_symbols_for_win.grid_remove()
        self.dropdown_symbols_for_win_x.grid_remove()
        self.dropdown_symbols_for_win_y.grid_remove()
        self.dropdown_symbols_for_win_z.grid_remove()
        self.button_submit.grid_remove()
        self.canvas.grid(row=1, column=0)
        self.initialize_board()
        self.game_status = 1
        self.initialize_grid()

    def print_player_turn(self):
        self.canvas.delete("player_turn")
        self.canvas.create_text(self.size_of_box * self.board_matrix[0] / 2, self.size_of_box / 6, font="cmr 25 bold", fill=self.symbol_colors[self.player_turn],
                                text=f'Player turn is {self.player_turn + 1}', tags="player_turn")

    def initialize_board(self):
        self.canvas.config(width=self.size_of_box * self.board_matrix[0], height=self.size_of_box * self.board_matrix[1] + self.size_of_box / 2)
        self.button_reset = ttk.Button(self.root, text="Reset Board", command=self.click_reset_board, style='my.TButton')
        self.button_reset.grid(row=0, column=0, padx=10, pady=10, sticky=SW)

        self.button_reset2 = ttk.Button(self.root, text="Reset Results", command=self.click_reset_results, style='my.TButton')
        self.button_reset2.grid(row=0, column=0, padx=0, pady=10, sticky=S)

        self.button_reset3 = ttk.Button(self.root, text="Reset Game", command=self.click_reset_game, style='my.TButton')
        self.button_reset3.grid(row=0, column=0, padx=10, pady=10, sticky=SE)

        # self.button_reset.place(x=self.size_of_box / 5, y=self.size_of_box / 7)
        self.player_turn = 0
        self.board_status = np.zeros(shape=self.board_matrix) - 1
        self.starting_player = 0
        self.tie = False
        self.tie_score = 0
        self.player_wins = [False] * self.number_of_players
        self.player_scores = [0] * self.number_of_players
        self.last_winner = ()
    
    def initialize_grid(self):
        for i in range(self.board_matrix[0] - 1):
            self.canvas.create_line((i + 1) * self.size_of_box, self.size_of_box / 2, (i + 1) * self.size_of_box, self.size_of_box * self.board_matrix[1] + self.size_of_box / 2)
        for i in range(-1, self.board_matrix[1] - 1):
            self.canvas.create_line(0, (i + 1) * self.size_of_box + self.size_of_box / 2, self.size_of_box * self.board_matrix[0], (i + 1) * self.size_of_box + self.size_of_box / 2)
        self.print_player_turn()

    def play_again(self):
        self.starting_player += 1
        if self.starting_player == self.number_of_players:
            self.starting_player = 0
        self.player_turn = self.starting_player
        self.board_status = np.zeros(shape=self.board_matrix) - 1
        self.initialize_grid()

    def draw_x(self, grid_position, color):
        self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size, grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size,
                                width=self.symbol_thickness, fill=color, tags="symbols")
        self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] + self.symbol_size, grid_position[0] + self.symbol_size, grid_position[1] - self.symbol_size,
                                width=self.symbol_thickness, fill=color, tags="symbols")

    def draw_o(self, grid_position, color):
        self.canvas.create_oval(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size, grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size,
                                width=self.symbol_thickness, outline=color, tags="symbols")

    def draw_rc(self, grid_position, color):
        self.canvas.create_rectangle(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size, grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size,
                                     width=self.symbol_thickness, outline=color, tags="symbols")

    def draw_player(self, player_number, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        if player_number % 3 == 0:
            self.draw_x(grid_position, self.symbol_colors[player_number])
        elif player_number % 3 == 1:
            self.draw_o(grid_position, self.symbol_colors[player_number])
        else:
            self.draw_rc(grid_position, self.symbol_colors[player_number])

    def display_gameover(self):
        text = "It's a tie"
        color = self.generic_color
        for i in range(self.number_of_players):
            if self.player_wins[i]:
                self.player_scores[i] += 1
                text = f'Winner: Player {i + 1}'
                color = self.symbol_colors[i]
        if not any(self.player_wins):
            self.tie_score += 1

        self.canvas.delete("all")
        self.canvas.create_text(self.size_of_box * self.board_matrix[0] / 2, self.size_of_box * self.board_matrix[1] / 8, font="cmr 40 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.size_of_box * self.board_matrix[0] / 2, self.size_of_box * self.board_matrix[1] / 4, font="cmr 30 bold", fill=self.green_color, text=score_text)

        score_text = ''
        for i in range(self.number_of_players):
            score_text += f'Player {i + 1}:\t\t' + str(self.player_scores[i]) + '\n'
        score_text += 'Tie:\t\t' + str(self.tie_score)
        self.canvas.create_text(self.size_of_box * self.board_matrix[0] / 2, 2 * self.size_of_box * self.board_matrix[1] / 4, font="cmr 25 bold", fill=self.green_color, text=score_text)
        self.game_status = 3

        score_text = 'Click to play again \n'
        self.canvas.create_text(self.size_of_box * self.board_matrix[0] / 2, 15 * self.size_of_box * self.board_matrix[1] / 16, font="cmr 20 bold", fill=self.generic_color, text=score_text)

    def convert_logical_to_grid_position_for_line(self, logical_position):
        grid_position = np.array(logical_position) * self.size_of_box + self.size_of_box / 2
        grid_position[0][1] += self.size_of_box / 2
        grid_position[1][1] += self.size_of_box / 2
        return list(grid_position)

    def convert_logical_to_grid_position(self, logical_position):
        grid_position = logical_position * self.size_of_box + self.size_of_box / 2
        return grid_position[0], grid_position[1] + self.size_of_box / 2

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array([grid_position[0], int(grid_position[1] - self.size_of_box / 2)])
        return np.array(grid_position // self.size_of_box, dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != -1

    def is_winner(self, player):
        # Check row:
        for x in range(self.board_matrix[1]):
            for z in range(self.board_matrix[0] - self.symbols_for_win[0] + 1):
                if all([self.board_status[n + z][x] == player for n in range(self.symbols_for_win[0])]):
                    return [(z, x), (self.symbols_for_win[0] - 1 + z, x)]
        # Check column:
        for y in range(self.board_matrix[0]):
            for z in range(self.board_matrix[1] - self.symbols_for_win[1] + 1):
                if all([self.board_status[y][n + z] == player for n in range(self.symbols_for_win[1])]):
                    return [(y, z), (y, self.symbols_for_win[1] - 1 + z)]
        # Check diagonals:
        for x in range(self.board_matrix[0] - self.symbols_for_win[2] + 1):
            for y in range(self.board_matrix[1] - self.symbols_for_win[2] + 1):
                if all([self.board_status[n + x][n + y] == player for n in range(self.symbols_for_win[2])]):
                    return [(x, y), (x + self.symbols_for_win[2] - 1, y + self.symbols_for_win[2] - 1)]
                if all([self.board_status[n + x][self.symbols_for_win[2] - 1 - n + y] == player for n in range(self.symbols_for_win[2])]):
                    return [(x, self.symbols_for_win[2] - 1 + y), (x + self.symbols_for_win[2] - 1, y)]
        return False

    def is_tie(self):
        r, c = np.where(self.board_status == -1)
        tie = False
        if len(r) == 0:
            tie = True
        return tie

    def is_gameover(self):
        self.last_winner = self.is_winner(self.player_turn)
        self.player_wins[self.player_turn] = bool(self.last_winner)
        if not any(self.player_wins):
            self.tie = self.is_tie()
        return any(self.player_wins) or self.tie

    def click(self, event):
        print(f'game_status = {self.game_status}')
        if self.game_status == 0:
            pass
        elif self.game_status == 1:
            if self.size_of_box / 2 < event.y < self.board_matrix[1] * self.size_of_box + self.size_of_box / 2 and event.x < self.board_matrix[0] * self.size_of_box:
                grid_position = [event.x, event.y]
                logical_position = self.convert_grid_to_logical_position(grid_position)
                if not self.is_grid_occupied(logical_position):
                    if not bool(self.last_winner):
                        self.draw_player(self.player_turn, logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = self.player_turn
                    if self.is_gameover():
                        self.game_status = 2
                        if bool(self.last_winner):
                            grid_position = self.convert_logical_to_grid_position_for_line(self.last_winner)
                            self.canvas.create_line(grid_position[0][0], grid_position[0][1], grid_position[1][0], grid_position[1][1], width=self.symbol_thickness / 3)
                            self.canvas.delete("player_turn")
                            self.canvas.create_text(self.size_of_box * self.board_matrix[0] / 2, self.size_of_box / 4, font="cmr 30 bold", fill=self.symbol_colors[self.player_turn],
                                                    text=f'The winner is player number {self.player_turn + 1}!', tags="player_turn")
                        else:
                            self.canvas.delete("player_turn")
                            self.canvas.create_text(self.size_of_box * self.board_matrix[0] / 2, self.size_of_box / 4, font="cmr 30 bold", text=f'It is a tie!', tags="player_turn")
                    else:
                        self.player_turn += 1
                        if self.player_turn == self.number_of_players:
                            self.player_turn = 0
                        self.print_player_turn()
        elif self.game_status == 2:
            self.display_gameover()
            self.player_wins = [False] * self.number_of_players
            self.last_winner = ()
            self.game_status = 3
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.game_status = 1

    # ## Reset game
    def click_reset_game(self):
        self.canvas.delete("all")
        self.canvas.grid_remove()
        self.button_reset.grid_remove()
        self.button_reset2.grid_remove()
        self.button_reset3.grid_remove()
        self.game_status = 0
        self.show_welcome_canvas()

    # ## Reset board
    def click_reset_board(self):
        self.canvas.delete("symbols")
        self.board_status = np.zeros(shape=self.board_matrix) - 1

    # ## Reset results
    def click_reset_results(self):
        self.player_scores = [0] * self.number_of_players
        self.tie_score = 0

    def click_reset_mouse(self, _):
        self.click_reset_game()


game_instance = Tk()
app = TicTacToe(game_instance)
game_instance.mainloop()
