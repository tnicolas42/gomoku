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

class G:  # class with all global variables
    # if a player destroy STONES_DESTROYED_VICTORY -> he win
    STONES_DESTROYED_VICTORY = 10

    # if a player align at least NB_ALIGNED_VICTORY and if there is no way to destroy the aligned stones -> he win
    NB_ALIGNED_VICTORY = 5

    # the number of squares arround taked pos to limit search zone
    NB_SQUARE_ARROUND = 1

    # the depth of the algorithm
    DEPTH = 3

    # used to count more the positive or negative action in heuristic
    H_POSITIVE_MULTIPLIER = 1  # positive number
    H_NEGATIVE_MULTIPLIER = -2  # negative number

    # on heuristic
    H_SELECT_TWO = 10 // 2  # .AA. BAA.
    H_SELECT_FREE_TWO = 15 // 2  # .AA. BAA.
    H_SELECT_THREE = 30 // 3  # BAAA.
    H_SELECT_FREE_THREE = 80 // 3  # .AAA. .A.AA.
    H_SELECT_FREE_FOUR = 300 // 4  # .AAAA.
    H_SELECT_FOUR = 100 // 4  # BAAAA. AA.AA
    H_SELECT_WIN = 1000 // 5  # AAAAA
    H_SELECT_VULNERABLILITY = -35  # BAA.
    H_SELECT_DESTROYED = 90  # ABBA -> A..A

    MINMAX_RANDOM_CHOICE = True  # choose a random position if we have the choice

    DEBUG_ANTICIPATION = False  # print the anticipation
    DEBUG_SEARCH_ZONE = False  # print the search zone