class Game(object):
    board = None  # the board
    players = None  # a list with the players

    def __init__(self, board, players):
        self.board = board
        self.players = players


    def run(self):
        while 42:
            self.board.print_board()
            for id_, player_act in enumerate(self.players):
                player_act.move()
                if player_act.has_win():
                    print("player %d has win" % (id_))
                    return True