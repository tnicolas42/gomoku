import tkinter as tk


class Gui(object):
    board = None
    win = None  # tk.Tk object
    w_board_sz = None  # size of board on window
    w_width_left = None  # width of left band
    board_canvas = None  # the canvas that contain the board
    left_canvas = None  # the canvas that contain the left band

    def __init__(self, board, title='gomoku', w_size_percent=80, left_band_w_percent=40):
        self.board = board

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

        self.update()


    def update(self):
        self.win.update()
        self.draw_board()


    def draw_board(self):
        # create bg
        self.board_canvas.create_rectangle(0, 0, self.w_board_sz, self.w_board_sz, fill="#F6AA49")

        # create lines
        line_space = self.w_board_sz / (self.board.size + 1)  # space btw 2 lines
        line_width = max(1, line_space / 10)
        x1 = line_space
        x2 = self.w_board_sz - line_space
        for i in range(self.board.size):
            y1 = line_space + line_space * i
            y2 = y1
            self.board_canvas.create_line(int(x1), int(y1), int(x2), int(y2), fill="black", width=line_width)

        y1 = line_space
        y2 = self.w_board_sz - line_space
        for i in range(self.board.size):
            x1 = line_space + line_space * i
            x2 = x1
            self.board_canvas.create_line(int(x1), int(y1), int(x2), int(y2), fill="black", width=line_width)

        # draw stones
        for y in range(self.board.size):
            for x in range(self.board.size):
                pass