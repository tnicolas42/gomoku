from srcs.players.player import Player


class RealPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)
        print("create real player")