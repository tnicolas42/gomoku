import time
import threading
from srcs.utils.stats import *

class Game(threading.Thread):
    """
    this is the main object
    this object contain a function to run the game
    """
    board = None  # the board
    players = None  # a list with the players
    gui = None  # the gui object
    id_player_act = 0  # id of the actual player
    quit = False

    def __init__(self):
        threading.Thread.__init__(self)

    def init(self, board, players, gui):
        """
        init the object with some variables
        """
        self.board = board
        self.players = players
        self.gui = gui

    @get_stats
    def run(self):
        """
        main function of the program
        this function run the game -> play all players turn, check if there is a winner, ...
        """
        while not self.quit:
            for id_, player_act in enumerate(self.players):
                if self.quit:
                    return False
                self.id_player_act = id_
                player_act.moving()

                # check for a winner in the game
                for id2_, player_act2 in enumerate(self.players):
                    if id2_ is not self.id_player_act and player_act2.has_win():
                        print(self.board)
                        print("player %d has win" % (id2_))
                        return True
                if player_act.has_win():
                    print(self.board)
                    print("player %d has win" % (self.id_player_act))
                    return True
                # check if this is the end of the game
                if self.board.remain_places <= 0:
                    print(self.board)
                    print("no winner in this game")
                    return False