import srcs.utils.color as c

# value for empty stones
STONE_EMPTY = -1

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
    BOARD_SZ = 19  # --board-size #
    PLAYERS = ["REAL", "AI"]  # --players REAL AI

    # if a player destroy STONES_DESTROYED_VICTORY -> he win
    STONES_DESTROYED_VICTORY = 10

    # if a player align at least NB_ALIGNED_VICTORY and if there is no way to destroy the aligned stones -> he win
    NB_ALIGNED_VICTORY = 5

    # the number of squares arround taked pos to limit search zone
    NB_SQUARE_ARROUND = 1

    # the depth of the algorithm
    DEPTH = 4

    # used to count more the positive or negative action in heuristic
    H_POSITIVE_MULTIPLIER = 1  # positive number
    H_NEGATIVE_MULTIPLIER = -1  # negative number

    # on heuristic
    H_SELECT_TWO = 10 // 2  # .AA. BAA.
    H_SELECT_FREE_TWO = 15 // 2  # .AA. BAA.
    H_SELECT_THREE = 30 // 3  # BAAA.
    H_SELECT_FREE_THREE = 80 // 3  # .AAA. .A.AA.
    H_SELECT_FREE_FOUR = 1500 // 4  # .AAAA.
    H_SELECT_FOUR = 100 // 4  # BAAAA. AA.AA
    H_SELECT_WIN = 6000 // 5  # AAAAA
    H_SELECT_VULNERABLILITY = -35  # BAA. Multiplied by the number of destroyed stones + 1
    H_SELECT_DESTROYED = 150  # ABBA -> A..A Multiplied by the number of destroyed stones + 1

    H_SELECT_DESTROY_VICTORY_ADDER = 10  # if this is the last destroyed stone, mul this stone by H_SELECT_DESTROY_VICTORY_ADDER

    MINMAX_RANDOM_CHOICE = False  # choose a random position if we have the choice

    DEBUG_ANTICIPATION = False  # print the anticipation
    DEBUG_SEARCH_ZONE = False  # print the search zone
    DEBUG_KEEP_NODE_PERCENT = False
    SHOW_VULNERABILITY = False  # --show-vulnerability show the vulnerables stones

    ASK_VALIDATION = True  # --skip-validation ask before quit, go back to menu, ...

    ENABLE_KEEP_NODE_PERCENT = True  # enable the filter to keep only certains nodes
    KEEP_NODE_PERCENT = 0.2  # the percentage of node to keep (in minmax algo)