from tkinter import *
import numpy as np
import time

board_matrix = (3, 3)
number_of_players = 3
symbols_in_series_for_a_win = 2
size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 40
symbol_colors = ['#EE4035', '#0492CF', '#FF00CC']
Green_color = '#7BC043'
generic_color = 'gray'


class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_turn = 0
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

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.starting_player += 1
        if self.starting_player == number_of_players:
            self.starting_player = 0
        self.player_turn = self.starting_player
        self.board_status = np.zeros(shape=board_matrix) - 1

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_colors[0])
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_colors[0])

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_colors[1])

    def draw_rc(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_rectangle(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                     grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                     outline=symbol_colors[2])

    def draw_player(self, player_number, logical_position):
        if player_number == 0:
            self.draw_X(logical_position)
        elif player_number == 1:
            self.draw_O(logical_position)
        else:
            self.draw_rc(logical_position)

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
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 40 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 30 bold", fill=Green_color,
                                text=score_text)

        score_text = ''
        for i in range(number_of_players):
            score_text += f'Player {i + 1}:\t\t' + str(self.player_scores[i]) + '\n'
        score_text += 'Tie:\t\t' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 25 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != -1

    def is_winner(self, player):
        for i in range(board_matrix[0]):
            if all([self.board_status[i][n] == player for n in range(board_matrix[1])]):
                return True
        for i in range(board_matrix[1]):
            if all([self.board_status[n][i] == player for n in range(board_matrix[0])]):
                return True

        if all([self.board_status[a][b] == player for a, b in zip(range(board_matrix[0]), range(board_matrix[1]))]):
            return True

        if all([self.board_status[a][b] == player for a, b in zip(range(board_matrix[0]), reversed(range(board_matrix[1])))]):
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == -1)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        for i in range(number_of_players):
            self.player_wins[i] = self.is_winner(i)
            if self.player_wins[i]:
                break
        if not any(self.player_wins):
            self.tie = self.is_tie()

        gameover = any(self.player_wins) or self.tie

        for i in range(number_of_players):
            if self.player_wins[i]:
                print(f'Player number {i + 1} wins')
        if self.tie:
            print('Its a tie')
        return gameover

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if not self.is_grid_occupied(logical_position):
                self.draw_player(self.player_turn, logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = self.player_turn
                self.player_turn += 1
                if self.player_turn == number_of_players:
                    self.player_turn = 0

            # Check if game is concluded
            if self.is_gameover():
                # print('Done')
                # time.sleep(0.2)
                self.display_gameover()
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = TicTacToe()
game_instance.mainloop()
