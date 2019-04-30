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
                self.gui.update()