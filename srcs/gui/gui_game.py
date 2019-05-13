import time
import tkinter as tk
from srcs.utils.utils import complementaryColor
from srcs.gui.base_gui import BaseGui
from srcs.const import *

class GuiGame(BaseGui):
    w_board_sz = None  # size of board on window
    w_width_left = None  # width of left band
    board_canvas = None  # the canvas that contain the board
    left_canvas = None  # the canvas that contain the left band
    last_pos = [None, None]
    error_pos = [[None, None], 0]  # to show an error (not well placed stone) -> [[x, y] time.time] -> the error is showed only for a limited time

    def __init__(self, game, gui, w_size_percent, left_band_w_percent):
        BaseGui.__init__(self, game=game, gui=gui)

        self.game.reinit()

        max_size = min(self.gui.win.winfo_screenwidth(), self.gui.win.winfo_screenheight())
        self.w_board_sz = int(max_size * (w_size_percent / 100))
        self.w_width_left = int(self.w_board_sz * (left_band_w_percent / 100))

        self.left_canvas = tk.Canvas(self, width=self.w_width_left, height=self.w_board_sz, bg="black")
        self.left_canvas.pack(side=tk.LEFT)

        self.board_canvas = tk.Canvas(self, width=self.w_board_sz, height=self.w_board_sz, bg="red")
        self.board_canvas.pack(side=tk.RIGHT)
        self.board_canvas.bind("<Button-1>", self.board_clicked)

    def board_clicked(self, event):
        """
        called when the mouse click on the board canvas
        get the position of the intersection under cursor and update update the player
        """
        line_space = self.w_board_sz / (G.BOARD_SZ + 1)
        x = (event.x - (line_space / 2)) / line_space
        y = (event.y - (line_space / 2)) / line_space
        if x >= G.BOARD_SZ or y >= G.BOARD_SZ or \
                event.x < line_space / 2 or event.y < line_space / 2:
            return
        # tell to the actual player that we click on this position
        self.game.players[self.game.id_player_act].clicked_on(int(x), int(y))

    def keyPress(self, e):
        if e.keysym in ("BackSpace", "Delete"):
            self.game.board.reset_debug()

    def draw(self):
        self.redraw()

    def redraw(self):
        """
        redraw all teh window
        """
        self.draw_board()
        self.draw_left_band()

    def draw_left_band(self):
        """
        redraw the left band
        """
        self.left_canvas.delete("all")

        for id_pl, player in enumerate(self.game.players):
            out_color = "grey"
            if id_pl == self.game.id_player_act:
                out_color = "red"
            self.left_canvas.create_rectangle(
                int(self.w_width_left * 0.1),
                int(self.w_board_sz / len(self.game.players) * id_pl + self.w_board_sz / len(self.game.players) * 0.05),
                int(self.w_width_left * 0.9),
                int(self.w_board_sz / len(self.game.players) * id_pl + self.w_board_sz / len(self.game.players) * 0.95),
                fill=STONES[id_pl], outline=out_color, width=self.w_board_sz/100)
            if self.game.board.nb_total_stones > 0:
                self.left_canvas.create_text(
                    int(self.w_width_left * 0.5),
                    int(self.w_board_sz / len(self.game.players) * id_pl + self.w_board_sz / len(self.game.players) * 0.15),
                    fill=complementaryColor(STONES[id_pl]), font="Times %d italic bold" % (self.w_width_left * 0.1),
                    text="Stones: %2d %2d%%" % (self.game.players[id_pl].nb_stone, (self.game.players[id_pl].nb_stone / self.game.board.nb_total_stones * 100)))
                self.left_canvas.create_text(
                    int(self.w_width_left * 0.5),
                    int(self.w_board_sz / len(self.game.players) * id_pl + self.w_board_sz / len(self.game.players) * 0.3),
                    fill=complementaryColor(STONES[id_pl]), font="Times %d italic bold" % (self.w_width_left * 0.1),
                    text="Capture: %d/%d" % (self.game.players[id_pl].destroyed_stones_count, G.STONES_DESTROYED_VICTORY))
                self.left_canvas.create_text(
                    int(self.w_width_left * 0.5),
                    int(self.w_board_sz / len(self.game.players) * id_pl + self.w_board_sz / len(self.game.players) * 0.45),
                    fill=complementaryColor(STONES[id_pl]), font="Times %d italic bold" % (self.w_width_left * 0.1),
                    text="%.2fs" % (self.game.players[id_pl].time_last_move))

    def draw_board(self):
        """
        redraw the board
        """
        self.board_canvas.delete("all")
        # create bg
        self.board_canvas.create_rectangle(0, 0, self.w_board_sz, self.w_board_sz, fill=BG_COLOR)

        # create lines an cols
        line_space = self.w_board_sz / (G.BOARD_SZ + 1)  # space btw 2 lines
        line_width = max(1, line_space / 10)
        x1 = line_space
        x2 = self.w_board_sz - line_space
        for i in range(G.BOARD_SZ):
            y1 = line_space + line_space * i
            y2 = y1
            self.board_canvas.create_line(int(x1), int(y1), int(x2), int(y2), fill="black", width=line_width)

        y1 = line_space
        y2 = self.w_board_sz - line_space
        for i in range(G.BOARD_SZ):
            x1 = line_space + line_space * i
            x2 = x1
            self.board_canvas.create_line(int(x1), int(y1), int(x2), int(y2), fill="black", width=line_width)

        # add point
        for x in range(G.BOARD_SZ // 2 % 6, G.BOARD_SZ, 6):
            for y in range(G.BOARD_SZ // 2 % 6, G.BOARD_SZ, 6):
                x_win = line_space + line_space * x
                y_win = line_space + line_space * y
                self.board_canvas.create_circle(int(x_win), int(y_win), int(line_space * 0.15), fill='black')

        # draw stones
        for y in range(G.BOARD_SZ):
            for x in range(G.BOARD_SZ):
                if self.game.board.content[y][x] >= 0:
                    x_win = line_space + line_space * x
                    y_win = line_space + line_space * y
                    create_args = {'fill': STONES[self.game.board.content[y][x]]}
                    if self.game.board.content_desc[y][x]['debug_color'] is not None:
                        create_args['outline'] = self.game.board.content_desc[y][x]['debug_color']
                        create_args['width'] = self.w_board_sz // 200
                    elif self.game.board.content_desc[y][x]['win']:
                        create_args['outline'] = 'green'
                        create_args['width'] = self.w_board_sz // 200
                    elif self.last_pos == [x, y]:
                        create_args['outline'] = 'blue'
                        create_args['width'] = self.w_board_sz // 200
                    elif G.SHOW_VULNERABILITY and self.game.board.content_desc[y][x]['vulnerability']:
                        create_args['outline'] = 'red'
                        create_args['width'] = self.w_board_sz // 200
                    self.board_canvas.create_circle(int(x_win), int(y_win), int(line_space * 0.4), **create_args)
                if self.error_pos[0] == [x, y]:
                    if self.error_pos[1] + 1 < time.time():
                        self.error_pos[0] = [None, None]
                    x_win = line_space + line_space * x
                    y_win = line_space + line_space * y
                    cross_line_args = {'fill': 'red', 'width': self.w_board_sz // 100}
                    self.board_canvas.create_line(int(x_win - line_space * 0.4), int(y_win - line_space * 0.4),
                                                    int(x_win + line_space * 0.4), int(y_win + line_space * 0.4),
                                                    **cross_line_args)
                    self.board_canvas.create_line(int(x_win + line_space * 0.4), int(y_win - line_space * 0.4),
                                                    int(x_win - line_space * 0.4), int(y_win + line_space * 0.4),
                                                    **cross_line_args)
                if self.game.board.content_desc[y][x]['debug_marker_color'] is not None:
                    x_win = line_space + line_space * x
                    y_win = line_space + line_space * y
                    cross_line_args = {'fill': self.game.board.content_desc[y][x]['debug_marker_color'], 'width': self.w_board_sz // 200}
                    self.board_canvas.create_line(int(x_win - line_space * 0.4), int(y_win - line_space * 0.4),
                                                    int(x_win + line_space * 0.4), int(y_win + line_space * 0.4),
                                                    **cross_line_args)
                    self.board_canvas.create_line(int(x_win + line_space * 0.4), int(y_win - line_space * 0.4),
                                                    int(x_win - line_space * 0.4), int(y_win + line_space * 0.4),
                                                    **cross_line_args)
