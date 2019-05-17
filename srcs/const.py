import srcs.utils.color as c

# value for empty stones
STONE_EMPTY = 0

# color for all stones (the max number of players is len(STONES))
STONES = (
    "#000000",
    "#ffffff",
    "#FF0000",
    "#00FF00",
    "#0000FF",
    "#FFFF00",
    "#FF00FF",
    "#00FFFF",
)

BG_COLOR = "#F6AA49"

class G:  # class with all global variables
    PLAYERS = ["REAL", "AI"]  # --players REAL AI

    MINMAX_RANDOM_CHOICE = False  # choose a random position if we have the choice

    DEBUG_ANTICIPATION = False  # print the anticipation
    DEBUG_SEARCH_ZONE = False  # print the search zone
    DEBUG_KEEP_NODE_PERCENT = False  # show the possible point to put stones
    DEBUG_PRINT_STATE = True  # print the state at the start of the game
    SHOW_VULNERABILITY = False  # --show-vulnerability show the vulnerables stones

    ASK_VALIDATION = True  # --skip-validation ask before quit, go back to menu, ...

    SPACE_BEFORE_AI_PLAY = False  # before AI turn, the player need to press SPACE

    DIFICULTY_DEFAULT = dict(
        # game rules
        BOARD_SZ = 19,  # --board-size #
        NB_ALIGNED_VICTORY = 5,  # if a player align at least NB_ALIGNED_VICTORY and if there is no way to destroy the aligned stones -> he win
        STONES_DESTROYED_VICTORY = 10,  # if a player destroy STONES_DESTROYED_VICTORY -> he win

        # algo variables
        DEPTH = 4,  # the depth of the algorithm
        NB_SQUARE_ARROUND = 1,  # the number of squares arround taked pos to limit search zone
        ENABLE_KEEP_NODE_PERCENT = True,  # enable the filter to keep only certains nodes
        KEEP_NODE_PERCENT = 0.2,  # the percentage of node to keep (in minmax algo)
        MIN_KEEP_NODE = 3,  # keep at least MIN_KEEP_NODE nodes (if the percentage return less than MIN_KEEP_NODE)
        USE_MAX_KEEP_NODE = True,  # if True, use MAX_KEEP_NODE, else... no limit !
        MAX_KEEP_NODE = 7,  # keep max MAX_KEEP_NODE nodes (if the percentage return more than MAX_KEEP_NODE)

        # used to count more the positive or negative action in heuristic
        H_POSITIVE_MULTIPLIER = 1,  # positive number
        H_NEGATIVE_MULTIPLIER = -1,  # negative number

        # on heuristic
        H_SELECT_TWO = 10 // 2,  # .AA. BAA.
        H_SELECT_FREE_TWO = 15 // 2,  # .AA. BAA.
        H_SELECT_THREE = 30 // 3,  # BAAA.
        H_SELECT_FREE_THREE = 80 // 3,  # .AAA. .A.AA.
        H_SELECT_FREE_FOUR = 1500 // 4,  # .AAAA.
        H_SELECT_FOUR = 100 // 4,  # BAAAA. AA.AA
        H_SELECT_WIN = 6000 // 5,  # AAAAA
        H_SELECT_VULNERABLILITY = -35,  # BAA. Multiplied by the number of destroyed stones + 1
        H_SELECT_DESTROYED = 150,  # ABBA -> A..A Multiplied by the number of destroyed stones + 1

        H_SELECT_DESTROY_VICTORY_ADDER = 10,  # if this is the last destroyed stone, mul this stone by H_SELECT_DESTROY_VICTORY_ADDER
    )
    DIFICULTY_LEVEL = [  # from easyer to harder
        dict(  # easy mode
            DEPTH = 2,
            H_SELECT_VULNERABLILITY = 0,
            H_SELECT_DESTROYED = 0,
            H_SELECT_DESTROY_VICTORY_ADDER = 0,
        ),
        dict(  # normal mode
            DEPTH = 2,
        ),
        dict(),  # hard mode (same as default)
    ]

    DIFICULTY = 1  # DIfICULTY_LEVEL[DIFICULTY]

    @staticmethod
    def GET(name):
        if name in G.DIFICULTY_LEVEL[G.DIFICULTY]:
            return G.DIFICULTY_LEVEL[G.DIFICULTY][name]
        return G.DIFICULTY_DEFAULT[name]

    @staticmethod
    def SET(name, val):
        if name in G.DIFICULTY_LEVEL[G.DIFICULTY]:
            G.DIFICULTY_LEVEL[G.DIFICULTY][name] = val
        elif name in G.DIFICULTY_DEFAULT:
            G.DIFICULTY_DEFAULT[name] = val
        else:
            print("ERROR in G.SET(" + name + ", " + str(val) + ")")
            exit(1)

    @staticmethod
    def PRINT_STATE():
        print("play on a board of %d*%d.\nWin conditions:\n\t- %d or more stones aligned (if at least one stone is vulnerable, the other player have one turn to destroy it)\n\t- %d stones destroyed" %
              (G.GET("BOARD_SZ"), G.GET("BOARD_SZ"), G.GET("NB_ALIGNED_VICTORY"), G.GET("STONES_DESTROYED_VICTORY")))
        if len(G.PLAYERS) == 2 and "AI" in G.PLAYERS:
            print("using MinMax algorithm: depth: %d. AI dificulty: %d/%d: %s vs %s" %
                  (G.GET("DEPTH"), G.DIFICULTY, len(G.DIFICULTY_LEVEL)-1, G.PLAYERS[0], G.PLAYERS[1]))
            if G.SPACE_BEFORE_AI_PLAY:
                print("for the IA turn, press space to start calculation")
            if G.SHOW_VULNERABILITY:
                print("to help you, the vulnerables stones are highlight")
        else:
            print("%d players, no AI" % (len(G.PLAYERS)))
        print()