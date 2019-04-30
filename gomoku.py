#!/usr/bin/python3
import sys
import argparse
from srcs.players.real_player import RealPlayer
from srcs.players.ai_player import AIPlayer
from srcs.utils.stats import EnableStats, print_stats
from srcs.board import Board
from srcs.game import Game
from srcs.gui import Gui
from srcs.const import *

player_types = dict(
    REAL=RealPlayer,
    AI=AIPlayer,
)
board = None
players = [None, None]
gui = None
game = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', type=str, default="REAL", choices=player_types.keys(),
                            help="This is the player 1 type (if REAL, this is a real player else, this is an AI)")
    parser.add_argument('--player2', type=str, default="REAL", choices=player_types.keys(),
                            help="This is the player 2 type (if REAL, this is a real player else, this is an AI)")
    parser.add_argument('--board-size', type=int, default=19,
                            help="this is the size of the board")

    parser.add_argument("--w-size-percent", type=int, default=80, choices=range(30,101), metavar="[30-100]",
                        help="Size of the gui windows (percentage of computer height)")
    parser.add_argument("-s", "--stats", action="store_true", default=False,
                        help="Print stats about functions [for debug]")

    args = parser.parse_args()
    EnableStats.enable = args.stats

    board = Board(size=args.board_size)
    players[0] = player_types[args.player1](board=board, stone=0)
    players[1] = player_types[args.player2](board=board, stone=1)
    gui = Gui(board=board, w_size_percent=args.w_size_percent)
    game = Game(board=board, players=players, gui=gui)

    game.run()
    while 1:
        pass

    print_stats()
