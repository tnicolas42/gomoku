import tkinter as tk
from srcs.const import *


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle


class Gui(object):
    game = None  # the game object
    win = None  # tk.Tk object
    w_board_sz = None  # size of board on window
    w_width_left = None  # width of left band
    board_canvas = None  # the canvas that contain the board
    left_canvas = None  # the canvas that contain the left band

    def __init__(self, game, title='gomoku', w_size_percent=80, left_band_w_percent=40):
        self.game = game

        self.win = tk.Tk()
        self.win.title = title
        max_size = min(self.win.winfo_screenwidth(), self.win.winfo_screenheight())
        self.w_board_sz = int(max_size * (w_size_percent / 100))
        self.w_width_left = int(self.w_board_sz * (left_band_w_percent / 100))

        self.win.geometry(str(self.w_board_sz + self.w_width_left) + 'x' + str(self.w_board_sz))
        self.win.resizable(0, 0) # Don't allow resizing in the x or y direction

        self.left_canvas = tk.Canvas(self.win, width=self.w_width_left, height=self.w_board_sz, bg="black")
        self.left_canvas.pack(side=tk.LEFT)

        self.board_canvas = tk.Canvas(self.win, width=self.w_board_sz, height=self.w_board_sz, bg="red")
        self.board_canvas.pack(side=tk.RIGHT)
        self.board_canvas.bind("<Button-1>", self.button_clicked)

    def button_clicked(self, event):
        line_space = self.w_board_sz / (self.game.board.size + 1)
        x = (event.x - (line_space / 2)) / line_space
        y = (event.y - (line_space / 2)) / line_space
        if x >= self.game.board.size or y >= self.game.board.size or \
                event.x < line_space / 2 or event.y < line_space / 2:
            return
        self.game.players[self.game.id_player_act].clicked_on(int(x), int(y))

    def update(self):
        self.win.update()
        self.draw_board()


    def draw_board(self):
        # create bg
        self.board_canvas.create_rectangle(0, 0, self.w_board_sz, self.w_board_sz, fill="#F6AA49")

        # create lines
        line_space = self.w_board_sz / (self.game.board.size + 1)  # space btw 2 lines
        line_width = max(1, line_space / 10)
        x1 = line_space
        x2 = self.w_board_sz - line_space
        for i in range(self.game.board.size):
            y1 = line_space + line_space * i
            y2 = y1
            self.board_canvas.create_line(int(x1), int(y1), int(x2), int(y2), fill="black", width=line_width)

        y1 = line_space
        y2 = self.w_board_sz - line_space
        for i in range(self.game.board.size):
            x1 = line_space + line_space * i
            x2 = x1
            self.board_canvas.create_line(int(x1), int(y1), int(x2), int(y2), fill="black", width=line_width)

        # draw stones
        for y in range(self.game.board.size):
            for x in range(self.game.board.size):
                if self.game.board.content[y][x] >= 0:
                    x_win = line_space + line_space * x
                    y_win = line_space + line_space * y
                    self.board_canvas.create_circle(int(x_win), int(y_win), int(line_space * 0.4), fill=STONES[self.game.board.content[y][x]])