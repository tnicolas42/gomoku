import threading
import time

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



    def run(self):
        """
        main function of the program
        this function run the game -> play all players turn, check if there is a winner, ...
        """
        while not self.quit:
            for id_, player_act in enumerate(self.players):
                self.id_player_act = id_
                player_act.move()
                if player_act.has_win():
                    self.board.print_board()
                    print("player %d has win" % (self.id_player_act))
                    return True
                if self.board.remain_places <= 0:
                    self.board.print_board()
                    print("no winner in this game")
                    return False