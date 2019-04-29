#!/usr/bin/python3
import sys
import argparse
from srcs.players.real_player import RealPlayer
from srcs.players.ai_player import AIPlayer
from srcs.board import Board
from srcs.game import Game
from srcs.const import *

player_types = dict(
    REAL=RealPlayer,
    AI=AIPlayer,
)
board = None
players = [None, None]
game = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', type=str, default="REAL", choices=player_types.keys(),
                            help="This is the player 1 type (if REAL, this is a real player else, this is an AI)")
    parser.add_argument('--player2', type=str, default="REAL", choices=player_types.keys(),
                            help="This is the player 2 type (if REAL, this is a real player else, this is an AI)")
    parser.add_argument('--board-size', type=int, default=19,
                            help="this is the size of the board")

    args = parser.parse_args()

    board = Board(size=args.board_size)
    players[0] = player_types[args.player1](board=board, stone=STONE_WHITE)
    players[1] = player_types[args.player2](board=board, stone=STONE_BLACK)

    game = Game(board=board, players=players)

    game.run()
