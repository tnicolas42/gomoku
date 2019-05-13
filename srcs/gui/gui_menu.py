import time
import tkinter as tk
from srcs.gui.base_gui import BaseGui
from srcs.const import *

class GuiMenu(BaseGui):
    size_board_scale = None
    size_board = None
    nb_players_scale = None
    nb_players = None
    playerAICheck = [None, None]
    playerAI = [None, None]
    depth_scale = None
    depth = None
    show_vul_check = None
    show_vul = None
    validateButton = None

    def __init__(self, game, gui):
        BaseGui.__init__(self, game=game, gui=gui, bg=BG_COLOR)
        self.size_board = tk.IntVar()
        self.nb_players = tk.IntVar()
        self.playerAI = [tk.BooleanVar(), tk.BooleanVar()]
        self.depth = tk.IntVar()
        self.show_vul = tk.BooleanVar()

    def keyPress(self, e):
        if e.keysym == "Return":
            self.launch_game()

    def draw(self):
        scale_args = dict(
            orient=tk.HORIZONTAL,
            length=int(self.gui.w_width * 0.75),
            showvalue=True,
            bg=BG_COLOR,
            font="Arial %d italic bold" % (self.gui.w_height * 0.05),
        )
        check_args = dict(
            bg=BG_COLOR,
            font="Arial %d italic bold" % (self.gui.w_height * 0.05),
        )
        txt_args = dict(
            font="Arial %d italic bold" % (self.gui.w_height * 0.05),
        )

        self.size_board_scale = tk.Scale(self, from_=2, to=50,
                                         label="size of the board (default: 19x19)",
                                         variable=self.size_board,
                                         **scale_args)
        self.size_board_scale.set(G.BOARD_SZ)
        self.size_board_scale.pack(pady=3)

        self.nb_players_scale = tk.Scale(self, from_=2, to=8,
                                         label="number of players (if > 2 you can't use AI)",
                                         variable=self.nb_players,
                                         **scale_args)
        self.nb_players_scale.set(len(G.PLAYERS))
        self.nb_players_scale.pack()

        self.playerAICheck[0] = tk.Checkbutton(self,
                                          variable=self.playerAI[0],
                                          text="player 1 AI (only for 2 players)",
                                          **check_args)
        if G.PLAYERS[0] == "AI":
            self.playerAICheck[0].select()
        else:
            self.playerAICheck[0].deselect()
        self.playerAICheck[0].pack()

        self.playerAICheck[1] = tk.Checkbutton(self,
                                          variable=self.playerAI[1],
                                          text="player 2 AI (only for 2 players)",
                                          **check_args)
        if G.PLAYERS[1] == "AI":
            self.playerAICheck[1].select()
        else:
            self.playerAICheck[1].deselect()
        self.playerAICheck[1].pack()

        self.depth_scale = tk.Scale(self, from_=1, to=15,
                                         label="depth",
                                         variable=self.depth,
                                         **scale_args)
        self.depth_scale.set(G.DEPTH)
        self.depth_scale.pack()

        self.show_vul_check = tk.Checkbutton(self,
                                             variable=self.show_vul,
                                             text="show vulnerable stones",
                                             **check_args)
        if G.SHOW_VULNERABILITY:
            self.show_vul_check.select()
        else:
            self.show_vul_check.deselect()
        self.show_vul_check.pack()

        self.create_text(
                    int(self.gui.w_width * 0.5),
                    int(self.gui.w_height * 0.9),
                    text="press enter to play",
                    **txt_args)

    def redraw(self):
        if self.nb_players.get() != 2:
            self.playerAICheck[0].deselect()
            self.playerAICheck[1].deselect()
            self.playerAICheck[0]['state'] = tk.DISABLED
            self.playerAICheck[1]['state'] = tk.DISABLED
        else:
            self.playerAICheck[0]['state'] = tk.ACTIVE
            self.playerAICheck[1]['state'] = tk.ACTIVE

    def launch_game(self):
        self.gui.openGame()

    def before_quit(self):
        G.BOARD_SZ = self.size_board.get()
        G.PLAYERS = ["REAL" for i in range(self.nb_players.get())]
        for i, plAI in enumerate(self.playerAI):
            if plAI.get() == True:
                G.PLAYERS[i] = "AI"
        G.DEPTH = self.depth.get()
        G.SHOW_VULNERABILITY = self.show_vul.get()