#!/usr/bin/python3
import sys
import time
import argparse
from srcs.utils.stats import EnableStats, print_stats
from srcs.board import Board
from srcs.game import Game, player_types
from srcs.gui.main_gui import Gui
from srcs.const import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=str, choices=player_types.keys(), nargs='+', required=False, default=G.PLAYERS,
                            help="this is the players list (--players AI REAL ...) -> max %d players" % (len(STONES)))

    parser.add_argument('--board-size', type=int, default=G.GET("BOARD_SZ"), choices=range(1,51), metavar="[1-50]",
                            help="this is the size of the board")
    parser.add_argument('--dificulty', type=int, default=G.DIFICULTY, choices=range(0,len(G.DIFICULTY_LEVEL)), metavar="[0-%d]" % (len(G.DIFICULTY_LEVEL)),
                            help="this is the dificulty level")

    parser.add_argument("--w-size-percent", type=int, default=80, choices=range(30,101), metavar="[30-100]",
                        help="Size of the gui windows (percentage of computer height)")
    parser.add_argument("-s", "--stats", action="store_true", default=False,
                        help="Print stats about functions [for debug]")

    parser.add_argument("--show-vulnerability", action="store_true", default=False,
                        help="Show vulnerable stones")

    parser.add_argument("--skip-menu", action="store_true", default=False,
                        help="Skip the menu and launch the game")

    parser.add_argument("--skip-validations", action="store_false", default=True,
                        help="Skip the validations for quit game, go back to menu, ...")

    args = parser.parse_args()
    if len(args.players) < 2 or len(args.players) > len(STONES):
        print("invalid number of players in the game (%d)" % (len(args.players)))
        exit(1)
    EnableStats.enable = args.stats

    G.DIFICULTY = args.dificulty
    G.SET("BOARD_SZ", args.board_size)
    G.ASK_VALIDATION = args.skip_validations
    G.SHOW_VULNERABILITY = args.show_vulnerability
    if len(args.players) >= 2:
        G.PLAYERS = args.players

    game = Game()
    gui = Gui(game=game, w_size_percent=args.w_size_percent, skip_menu=args.skip_menu)
    game.gui = gui

    game.start()
    gui.run()
    game.join()

    print_stats()
