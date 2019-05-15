import os
import time
import tkinter as tk
from tkinter import messagebox
from platform import system as platform
from srcs.gui.gui_game import GuiGame
from srcs.gui.gui_menu import GuiMenu
from srcs.utils.clock import Clock
from srcs.const import *


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle


class Gui(object):
    """
    this object is used for the gui -> draw the game o the screen and get mouse & keyboard events
    """
    game = None  # the game object
    win = None  # tk.Tk object
    w_width = None  # size of board on window
    w_height = None  # width of left band
    w_size_percent = None
    left_band_w_percent = None
    clock = None  # this is a clock object to control time

    gui_game = None
    gui_menu = None
    gui_act = None  # pointer on the actual gui

    def __init__(self, game, title='gomoku', skip_menu=False, w_size_percent=80, left_band_w_percent=40, rate=10):
        self.game = game

        self.clock = Clock(rate=rate)

        self.win = tk.Tk()
        self.win.title(title)
        max_size = min(self.win.winfo_screenwidth(), self.win.winfo_screenheight())
        self.w_height = int(max_size * (w_size_percent / 100))
        self.w_width = int(max_size * (w_size_percent / 100)) + int(self.w_height * (left_band_w_percent / 100))
        self.w_size_percent = w_size_percent
        self.left_band_w_percent = left_band_w_percent

        self.win.geometry(str(self.w_width) + 'x' + str(self.w_height))
        self.win.resizable(0, 0) # Don't allow resizing in the x or y direction

        self.win.protocol("WM_DELETE_WINDOW", self.on_closing_window)

        # key binding
        self.win.bind('<Key>', self.keyPress)

        if skip_menu:
            self.openGame()
        else:
            self.openMenu()

        # center the win
        self.centerWindows()
        # focus the win
        if platform() == 'Darwin':  # How Mac OS X is identified by Python
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def openMenu(self):
        if self.gui_act is not None:
            self.gui_act.before_quit()
        self.gui_menu = GuiMenu(game=self.game, gui=self)
        self.gui_menu.pack(fill=tk.BOTH, expand=1)
        tmp = self.gui_act
        self.gui_act = self.gui_menu
        self.gui_act.draw()
        if tmp is not None:
            tmp.destroy()
            del tmp

    def openGame(self):
        if self.gui_act is not None:
            self.gui_act.before_quit()
        self.gui_game = GuiGame(game=self.game, gui=self, w_size_percent=self.w_size_percent, left_band_w_percent=self.left_band_w_percent)
        self.gui_game.pack(fill=tk.BOTH, expand=1)
        tmp = self.gui_act
        self.gui_act = self.gui_game
        self.gui_act.draw()
        if tmp is not None:
            tmp.destroy()
            del tmp

    def run(self):
        """
        main gui function:
        this function update the gui at a given rate
        """
        while not self.game.quit:
            if self.gui_act is not None:
                self.update()
                self.redraw()
            self.clock.tick()  # wait until next loop

    def on_closing_window(self):
        if not G.ASK_VALIDATION or messagebox.askokcancel("do you want to quit ?"):
            self.game.quit = True
            self.game.reset_game = True

    def keyPress(self, e):
        if e.keysym == "Escape":
            self.on_closing_window()
        else:
            self.gui_act.keyPress(e)

    def update(self):
        """
        update all events (mouse click, keydown, ...)
        """
        self.win.update()

    def redraw(self):
        self.gui_act.redraw()


    def centerWindows(self):
        """
        "center" the windows in the middle of the screen
        """
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.win.winfo_screenwidth()/2 - self.w_width/2)
        positionDown = int(self.win.winfo_screenheight()/2 - self.w_height/2)

        # Positions the window in the center of the page.
        self.win.geometry("+{}+{}".format(positionRight, positionDown))
