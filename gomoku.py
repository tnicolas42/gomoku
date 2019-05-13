#!/usr/bin/python3
import sys
import time
import argparse
from srcs.utils.stats import EnableStats, print_stats
from srcs.players.real_player import RealPlayer
from srcs.players.ai_player import AIPlayer
from srcs.board import Board
from srcs.game import Game
from srcs.gui import Gui
from srcs.const import *

player_types = dict(
    REAL=RealPlayer,
    AI=AIPlayer,
)
board = None
players = []
gui = None
game = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=str, choices=player_types.keys(), nargs='+', required=False, default=["REAL", "AI"],
                            help="this is the players list (--players AI REAL ...) -> max %d players" % (len(STONES)))

    parser.add_argument('--board-size', type=int, default=19, choices=range(1,101), metavar="[1-100]",
                            help="this is the size of the board")

    parser.add_argument("--w-size-percent", type=int, default=80, choices=range(30,101), metavar="[30-100]",
                        help="Size of the gui windows (percentage of computer height)")
    parser.add_argument("-s", "--stats", action="store_true", default=False,
                        help="Print stats about functions [for debug]")

    parser.add_argument("--show-vulnerability", action="store_true", default=False,
                        help="Show vulnerable stones")

    args = parser.parse_args()
    if len(args.players) < 2 or len(args.players) > len(STONES):
        print("invalid number of players in the game (%d)" % (len(args.players)))
        exit(1)
    EnableStats.enable = args.stats

    game = Game()
    board = Board(game=game, size=args.board_size)
    for id_, player in enumerate(args.players):
        players.append(player_types[player](game=game, stone=id_))
    gui = Gui(game=game, w_size_percent=args.w_size_percent, show_vulnerability=args.show_vulnerability)
    game.init(board=board, players=players, gui=gui)

    game.start()
    gui.run()
    game.quit = True

    print_stats()
