from tkinter import *
import numpy as np
import random
import time


# board_matrix = (2, 2)
# board_matrix = (3, 3)
# board_matrix = (4, 4)
board_matrix = (4, 3)
number_of_players = 2
symbols_in_series_for_a_win = 3
size_of_box = 200
symbol_size = (size_of_box - size_of_box / 3) / 2
symbol_thickness = 40
symbol_colors = ["#" + ''.join([random.choice('0123456789ABCDE') for h in range(6)]) for n in range(number_of_players)]     # F is too white
Green_color = '#7BC043'
generic_color = 'gray'


class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_box * board_matrix[0], height=size_of_box * board_matrix[1] + size_of_box / 2)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.player_turn = 0
        self.initialize_board()
        self.board_status = np.zeros(shape=board_matrix) - 1

        self.starting_player = 0
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.tie_score = 0
        self.player_wins = [False] * number_of_players
        self.player_scores = [0] * number_of_players

    def mainloop(self):
        self.window.mainloop()

    def print_player_turn(self):
        self.canvas.delete("player_turn")
        self.canvas.create_text(size_of_box * board_matrix[0] / 2, size_of_box * board_matrix[1] + size_of_box / 4, font="cmr 30 bold",
                                fill=symbol_colors[self.player_turn], text=f'Player turn is {self.player_turn + 1}', tags="player_turn")

    def initialize_board(self):
        for i in range(board_matrix[0] - 1):
            self.canvas.create_line((i + 1) * size_of_box, 0, (i + 1) * size_of_box, size_of_box * board_matrix[1])
        for i in range(board_matrix[1]):
            self.canvas.create_line(0, (i + 1) * size_of_box, size_of_box * board_matrix[0], (i + 1) * size_of_box)
        self.print_player_turn()

    def play_again(self):
        self.starting_player += 1
        if self.starting_player == number_of_players:
            self.starting_player = 0
        self.player_turn = self.starting_player
        self.board_status = np.zeros(shape=board_matrix) - 1
        self.initialize_board()


    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_X(self, grid_position, color):
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=color)

    def draw_O(self, grid_position, color):
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=color)

    def draw_rc(self, grid_position, color):
        self.canvas.create_rectangle(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                     grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                     outline=color)

    def draw_player(self, player_number, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        if player_number % 3 == 0:
            self.draw_X(grid_position, symbol_colors[player_number])
        elif player_number % 3 == 1:
            self.draw_O(grid_position, symbol_colors[player_number])
        else:
            self.draw_rc(grid_position, symbol_colors[player_number])

    def display_gameover(self):
        for i in range(number_of_players):
            if self.player_wins[i]:
                self.player_scores[i] += 1
                text = f'Winner: Player {i + 1}'
                color = symbol_colors[i]
        if not any(self.player_wins):
            self.tie_score += 1
            text = 'Its a tie'
            color = generic_color

        self.canvas.delete("all")
        self.canvas.create_text(size_of_box * board_matrix[0] / 2, size_of_box * board_matrix[1] / 8, font="cmr 40 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_box * board_matrix[0] / 2, size_of_box * board_matrix[1] / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)

        score_text = ''
        for i in range(number_of_players):
            score_text += f'Player {i + 1}:\t\t' + str(self.player_scores[i]) + '\n'
        score_text += 'Tie:\t\t' + str(self.tie_score)
        self.canvas.create_text(size_of_box * board_matrix[0] / 2, 2 * size_of_box * board_matrix[1] / 4, font="cmr 25 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_box * board_matrix[0] / 2, 15 * size_of_box * board_matrix[1] / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    @staticmethod
    def convert_logical_to_grid_position(logical_position):
        return logical_position * size_of_box + size_of_box / 2

    @staticmethod
    def convert_grid_to_logical_position(grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // size_of_box, dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != -1

    def is_winner(self, player):
        for i in range(board_matrix[0]):
            if all([self.board_status[i][n] == player for n in range(board_matrix[1])]):
                return True
        for i in range(board_matrix[1]):
            if all([self.board_status[n][i] == player for n in range(board_matrix[0])]):
                return True
        # Diagonals:
        y = 0
        z = 0
        # for y in range(abs(board_matrix[1] - board_matrix[0]) + 1):
        # for z in range(abs(board_matrix[1] - board_matrix[0]) + 1):
        if all([self.board_status[a][b] == player for a, b in zip(range(z, board_matrix[0] + z), range(y, board_matrix[1] + y))]):
            return True
        if all([self.board_status[a][b] == player for a, b in zip(range(z, board_matrix[0] + z), reversed(range(y, board_matrix[1] + y)))]):
            return True
        return False

    def is_tie(self):
        r, c = np.where(self.board_status == -1)
        tie = False
        if len(r) == 0:
            tie = True
        return tie

    def is_gameover(self):
        self.player_wins[self.player_turn] = self.is_winner(self.player_turn)
        if not any(self.player_wins):
            self.tie = self.is_tie()
        return any(self.player_wins) or self.tie

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        if logical_position[1] < board_matrix[1]:
            if not self.reset_board:
                if not self.is_grid_occupied(logical_position):
                    print('01')
                    self.draw_player(self.player_turn, logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = self.player_turn
                if self.is_gameover():      # Check if game is concluded
                    print('02')
                    # print('Done')
                    # time.sleep(0.2)
                    self.display_gameover()
                    self.player_wins = [False] * number_of_players
                else:
                    print('03')
                    self.player_turn += 1
                    if self.player_turn == number_of_players:
                        self.player_turn = 0
                    self.print_player_turn()
            else:  # Play Again
                self.canvas.delete("all")
                self.play_again()
                self.reset_board = False


game_instance = TicTacToe()
game_instance.mainloop()
