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

# if a player destroy STONES_DESTROYED_VICTORY -> he win
STONES_DESTROYED_VICTORY = 10

# if a player align at least NB_ALIGNED_VICTORY and if there is no way to destroy the aligned stones -> he win
NB_ALIGNED_VICTORY = 5

# the number of squares arround taked pos to limit search zone
NB_SQUARE_ARROUND = 2