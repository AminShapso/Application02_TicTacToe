from tkinter import *
import numpy as np
import random


number_of_players = 2
board_matrix = (3, 3)
symbols_in_series_for_a_win = (*board_matrix, min(board_matrix))
# symbols_in_series_for_a_win = (4, 4, 3)
size_of_box = 250 - int(sum(board_matrix) / 2) * 18
symbol_size = (size_of_box - size_of_box / 3) / 2
symbol_thickness = (size_of_box - size_of_box / 3) / 3
symbol_colors = ["#" + ''.join([random.choice('123456789ABCDE') for h in range(6)]) for n in range(number_of_players)]     # 0 and F are too extreme
Green_color = '#7BC043'
generic_color = 'gray'


class TicTacToe:
    canvas = None
    player_turn = None
    board_status = None
    starting_player = None
    tie = None
    tie_score = None
    player_wins = None
    player_scores = None
    last_winner = None

    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.bind('<Button-1>', self.click)      # user input

        self.initialize_board()
        self.game_status = 0
        self.show_welcome_canvas()
        # self.game_status = 1
        # self.initialize_grid()cut

    def mainloop(self):
        self.window.mainloop()

    def print_player_turn(self):
        self.canvas.delete("player_turn")
        self.canvas.create_text(size_of_box * board_matrix[0] / 2, size_of_box / 4, font="cmr 30 bold", fill=symbol_colors[self.player_turn],
                                text=f'Player turn is {self.player_turn + 1}', tags="player_turn")
    
    def initialize_board(self):
        self.canvas = Canvas(self.window, width=size_of_box * board_matrix[0], height=size_of_box * board_matrix[1] + size_of_box / 2)
        self.canvas.pack()

        self.player_turn = 0
        self.board_status = np.zeros(shape=board_matrix) - 1
        self.starting_player = 0
        self.tie = False
        self.tie_score = 0
        self.player_wins = [False] * number_of_players
        self.player_scores = [0] * number_of_players
        self.last_winner = ()
    
    def initialize_grid(self):
        for i in range(board_matrix[0] - 1):
            self.canvas.create_line((i + 1) * size_of_box, size_of_box / 2, (i + 1) * size_of_box, size_of_box * board_matrix[1] + size_of_box / 2)
        for i in range(-1, board_matrix[1] - 1):
            self.canvas.create_line(0, (i + 1) * size_of_box + size_of_box / 2, size_of_box * board_matrix[0], (i + 1) * size_of_box + size_of_box / 2)
        self.print_player_turn()

    def show_welcome_canvas(self):
        self.canvas.create_text(size_of_box * board_matrix[0] / 2, size_of_box / 2, font="cmr 60 bold", text='HELLO', tags='welcome')

    def play_again(self):
        self.starting_player += 1
        if self.starting_player == number_of_players:
            self.starting_player = 0
        self.player_turn = self.starting_player
        self.board_status = np.zeros(shape=board_matrix) - 1
        self.initialize_grid()

    def draw_x(self, grid_position, color):
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size, grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, fill=color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size, grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                width=symbol_thickness, fill=color)

    def draw_o(self, grid_position, color):
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size, grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, outline=color)

    def draw_rc(self, grid_position, color):
        self.canvas.create_rectangle(grid_position[0] - symbol_size, grid_position[1] - symbol_size, grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                     width=symbol_thickness, outline=color)

    def draw_player(self, player_number, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        if player_number % 3 == 0:
            self.draw_x(grid_position, symbol_colors[player_number])
        elif player_number % 3 == 1:
            self.draw_o(grid_position, symbol_colors[player_number])
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
        self.game_status = 3

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_box * board_matrix[0] / 2, 15 * size_of_box * board_matrix[1] / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    @staticmethod
    def convert_logical_to_grid_position_for_line(logical_position):
        grid_position = np.array(logical_position) * size_of_box + size_of_box / 2
        grid_position[0][1] += size_of_box / 2
        grid_position[1][1] += size_of_box / 2
        return list(grid_position)

    @staticmethod
    def convert_logical_to_grid_position(logical_position):
        grid_position = logical_position * size_of_box + size_of_box / 2
        return grid_position[0], grid_position[1] + size_of_box / 2

    @staticmethod
    def convert_grid_to_logical_position(grid_position):
        grid_position = np.array([grid_position[0], int(grid_position[1] - size_of_box / 2)])
        return np.array(grid_position // size_of_box, dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != -1

    def is_winner(self, player):
        # Check row:
        for x in range(board_matrix[1]):
            for z in range(board_matrix[0] - symbols_in_series_for_a_win[0] + 1):
                if all([self.board_status[n + z][x] == player for n in range(symbols_in_series_for_a_win[0])]):
                    return [(z, x), (symbols_in_series_for_a_win[0] - 1 + z, x)]
        # Check column:
        for y in range(board_matrix[0]):
            for z in range(board_matrix[1] - symbols_in_series_for_a_win[1] + 1):
                if all([self.board_status[y][n + z] == player for n in range(symbols_in_series_for_a_win[1])]):
                    return [(y, z), (y, symbols_in_series_for_a_win[1] - 1 + z)]
        # Check diagonals:
        for x in range(board_matrix[0] - symbols_in_series_for_a_win[2] + 1):
            for y in range(board_matrix[1] - symbols_in_series_for_a_win[2] + 1):
                if all([self.board_status[n + x][n + y] == player for n in range(symbols_in_series_for_a_win[2])]):
                    return [(x, y), (x + symbols_in_series_for_a_win[2] - 1, y + symbols_in_series_for_a_win[2] - 1)]
                if all([self.board_status[n + x][symbols_in_series_for_a_win[2] - 1 - n + y] == player for n in range(symbols_in_series_for_a_win[2])]):
                    return [(x, symbols_in_series_for_a_win[2] - 1 + y), (x + symbols_in_series_for_a_win[2] - 1, y)]
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
        game_status_DEBUG = self.game_status
        if self.game_status == 1:
            if size_of_box / 2 < event.y < board_matrix[1] * size_of_box + size_of_box / 2 and event.x < board_matrix[0] * size_of_box:
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
                            self.canvas.create_line(grid_position[0][0], grid_position[0][1], grid_position[1][0], grid_position[1][1], width=symbol_thickness / 3)
                            self.canvas.delete("player_turn")
                            self.canvas.create_text(size_of_box * board_matrix[0] / 2, size_of_box / 4, font="cmr 30 bold", fill=symbol_colors[self.player_turn],
                                                    text=f'The winner is player number {self.player_turn + 1}!!!', tags="player_turn")
                        else:
                            self.canvas.delete("player_turn")
                            self.canvas.create_text(size_of_box * board_matrix[0] / 2, size_of_box / 4, font="cmr 30 bold", text=f'It is a tie!', tags="player_turn")
                    else:
                        self.player_turn += 1
                        if self.player_turn == number_of_players:
                            self.player_turn = 0
                        self.print_player_turn()
        elif self.game_status == 2:
            self.display_gameover()
            self.player_wins = [False] * number_of_players
            self.last_winner = ()
            self.game_status = 3
        elif self.game_status == 0:
            print('HELLO')
            self.canvas.delete("welcome")
            self.initialize_board()
            self.canvas.delete("welcome")
            self.game_status = 1
            # board_matrix = (4, 4)
            self.initialize_grid()
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.game_status = 1
        print(f'game_status: before = {game_status_DEBUG} and after = {self.game_status}')


game_instance = TicTacToe()
game_instance.mainloop()
