import time

class Game(object):
    board = None  # the board
    players = None  # a list with the players
    gui = None  # the gui object
    id_player_act = 0  # id of the actual player

    def __init__(self):
        pass

    def init(self, board, players, gui):
        self.board = board
        self.players = players
        self.gui = gui



    def run(self):
        self.gui.update()
        while 42:
            self.board.print_board()
            for id_, player_act in enumerate(self.players):
                id_player_act = id_
                player_act.move()
                if player_act.has_win():
                    print("player %d has win" % (id_player_act))
                    return True
                self.gui.update()