import time

class Game(object):
    board = None  # the board
    players = None  # a list with the players
    gui = None  # the gui object

    def __init__(self, board, players, gui):
        self.board = board
        self.players = players
        self.gui = gui



    def run(self):
        while 42:
            self.board.print_board()
            for id_, player_act in enumerate(self.players):
                player_act.move()
                if player_act.has_win():
                    print("player %d has win" % (id_))
                    return True
            self.gui.update()

            time.sleep(1)  # ##################################