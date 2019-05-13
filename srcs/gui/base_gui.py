import tkinter as tk


class BaseGui(tk.Canvas):
    game = None
    gui = None

    def __init__(self, game, gui, *args, **kwargs):
        self.game = game
        self.gui = gui
        tk.Canvas.__init__(self, self.gui.win,
                           width=self.gui.win.winfo_screenwidth(),
                           height=self.gui.win.winfo_screenheight(),
                           *args, **kwargs)


    def keyPress(self, e):
        pass

    def draw(self):
        pass

    def redraw(self):
        pass

    def before_quit(self):
        pass