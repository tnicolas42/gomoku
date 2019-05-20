from srcs.utils.stats import *
from srcs.const import *


def _check_aligned_dir(game, node, x, y, stone, addx, addy, check_return, multiplier=1):
    """
    used to calc heuristic
    """
    nb_aligned = 1  # number of aligned stones
    nb_almost_aligned = 1  # number of pseudo aligned stones (pseudo mean that there is a hole)
    free_side = [False, False]  # True if there is a free space around alignement
    nb_hole = [0, 0]
    new_x = x + addx
    new_y = y + addy
    while 1:
        # if out of bound
        if not (0 <= new_x < G.GET("BOARD_SZ") and 0 <= new_y < G.GET("BOARD_SZ")):
            if node.board.content[new_y - addy][new_x - addx] == STONE_EMPTY:
                free_side[0] = True
            break
        # if player stone
        elif node.board.content[new_y][new_x] == stone:
            nb_almost_aligned += 1
            if nb_hole[0] == 0:
                nb_aligned += 1
        # if empty
        elif node.board.content[new_y][new_x] == STONE_EMPTY:
            if node.board.content[new_y - addy][new_x - addx] == stone:
                if nb_hole[0] == 0:
                    nb_hole[0] = 1
                else:
                    free_side[0] = True
                    break
            elif node.board.content[new_y - addy][new_x - addx] == STONE_EMPTY:
                nb_hole[0] = 0
                free_side[0] = True
                break
        # if other stone
        else:
            if node.board.content[new_y - addy][new_x - addx] == STONE_EMPTY:
                nb_hole[0] = 0
                free_side[0] = True
            break
        new_x += addx
        new_y += addy
    new_x = x - addx
    new_y = y - addy
    while 1:
        # if out of bound
        if not (0 <= new_x < G.GET("BOARD_SZ") and 0 <= new_y < G.GET("BOARD_SZ")):
            if node.board.content[new_y + addy][new_x + addx] == STONE_EMPTY:
                free_side[0] = True
            break
        # if player stone
        elif node.board.content[new_y][new_x] == stone:
            nb_almost_aligned += 1
            if nb_hole[1] == 0:
                nb_aligned += 1
        # if empty
        elif node.board.content[new_y][new_x] == STONE_EMPTY:
            if node.board.content[new_y + addy][new_x + addx] == stone:
                if nb_hole[1] == 0:
                    nb_hole[1] = 1
                else:
                    free_side[1] = True
                    break
            elif node.board.content[new_y + addy][new_x + addx] == STONE_EMPTY:
                nb_hole[1] = 0
                free_side[1] = True
                break
        # if other stone
        else:
            if node.board.content[new_y + addy][new_x + addx] == STONE_EMPTY:
                nb_hole[1] = 0
                free_side[1] = True
            break
        new_x -= addx
        new_y -= addy

    if nb_aligned >= G.GET("NB_ALIGNED_VICTORY"):  # AAAAA
        if game.id_player_act == stone:
            node.is_win = True
        check_return['nb_win'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
    elif nb_aligned >= 4:
        if free_side[0] + free_side[1] == 2:  # .AAAA.
            check_return['nb_free_four'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
        elif free_side[0] + free_side[1] == 1:  # BAAAA.
            check_return['nb_four'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
    elif nb_aligned >= 3:
        if free_side[0] + free_side[1] == 2:  # .AAA.
            check_return['nb_free_three'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
        elif free_side[0] + free_side[1] == 1:  # BAAA.
            check_return['nb_three'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
    elif nb_aligned >= 2:
        if free_side[0] + free_side[1] == 2:  # .AA.
            check_return['nb_free_two'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
        elif free_side[0] + free_side[1] == 1:  # BAA.
            check_return['nb_two'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
    elif nb_almost_aligned >= 4:  # AA.AA  AAA.AA
        check_return['nb_four'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
    elif nb_almost_aligned == 3:
        if free_side[0] + free_side[1] == 2:  # .A.AA.  .AAA.
            check_return['nb_free_three'] += multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))

def _check_stone(game, node, x, y, check_return, multiplier=1):
    """
    on the stone, check ->
        the nb of free three
        the nb of free four
        the nb of win
        the number of vulnerability
    """
    stone = node.board.content[y][x]
    if stone == STONE_EMPTY:
        return

    if node.board.check_vulnerability(x, y):
        mul = 1
        if game.players[stone].destroyed_stones_count + 2 >= G.GET("STONES_DESTROYED_VICTORY"):
            mul = G.GET("H_SELECT_DESTROY_VICTORY_ADDER")
        check_return['nb_vulnerable'] += mul * (game.players[stone].destroyed_stones_count + 1) * multiplier * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
    _check_aligned_dir(game, node, x, y, stone, -1, 0, check_return, multiplier=multiplier)
    _check_aligned_dir(game, node, x, y, stone, 0, 1, check_return, multiplier=multiplier)
    _check_aligned_dir(game, node, x, y, stone, 1, 1, check_return, multiplier=multiplier)
    _check_aligned_dir(game, node, x, y, stone, 1, -1, check_return, multiplier=multiplier)


def get_hash(node):
    return hash(str(node.board.content))


def selective_heuristic(node, printDebug=False):
    """
    calc the heuristic with particular attention with the ordered posed stones
    """
    if node.heuristic is not None:
        return node.heuristic

    game = node.game
    check_return = dict(
        nb_two=0,
        nb_free_two=0,
        nb_three=0,
        nb_free_three=0,
        nb_free_four=0,
        nb_four=0,
        nb_win=0,
        nb_vulnerable=0,
        nb_destroyed=0,
    )

    node_hist = []  # from new to last
    tmp = node
    while tmp.parent:
        node_hist.append((tmp.x, tmp.y, int(tmp.stone)))
        tmp.is_stone_on_board = True
        if G.GET("ENABLE_KEEP_NODE_PERCENT"):
            break
        tmp = tmp.parent

    lenhist = len(node_hist)
    if lenhist > 1:
        node_hist.reverse()
    for i, (x, y, stone) in enumerate(node_hist):
        if node.board.is_allowed(x, y, stone):
            nb_destroyed = node.board.put_stone(x, y, stone, test=True)
            mul = ((lenhist+1)>>1) - (i>>1) + 1
            if nb_destroyed > 0:
                mul = 1
                if game.players[stone].destroyed_stones_count + nb_destroyed >= G.GET("STONES_DESTROYED_VICTORY"):
                    mul = G.GET("H_SELECT_DESTROY_VICTORY_ADDER")
                    if game.id_player_act == stone:
                        node.is_win = True
                check_return['nb_destroyed'] += mul * (game.players[stone].destroyed_stones_count + 1) * mul * nb_destroyed * (G.GET("H_POSITIVE_MULTIPLIER") if game.id_player_act == stone else G.GET("H_NEGATIVE_MULTIPLIER"))
            _check_stone(game, node, x, y, check_return,
                        multiplier=mul)
        else:
            return None

    hash_node = get_hash(node)
    if hash_node in node.transpositionTable:
        check_return = node.transpositionTable[hash_node]
    else:
        for x in range(G.GET("BOARD_SZ")):
            for y in range(G.GET("BOARD_SZ")):
                _check_stone(game, node, x, y, check_return)

    if hash_node not in node.transpositionTable:
        node.transpositionTable[hash_node] = check_return

    if printDebug:
        print(node.board)
        print(end="nb_two: %d " % (check_return['nb_two']))
        print(end="nb_free_two: %d " % (check_return['nb_free_two']))
        print(end="nb_three: %d " % (check_return['nb_three']))
        print(end="nb_free_three: %d " % (check_return['nb_free_three']))
        print(end="nb_four: %d " % (check_return['nb_four']))
        print(end="nb_free_four: %d " % (check_return['nb_free_four']))
        print(end="nb_destroyed: %d " % (check_return['nb_destroyed']))
        print(end="nb_vulnerable: %d " % (check_return['nb_vulnerable']))
        print(end="nb_win: %d " % (check_return['nb_win']))
        print()

    # apply a value
    check_return['nb_two'] *= G.GET("H_SELECT_TWO")
    check_return['nb_free_two'] *= G.GET("H_SELECT_FREE_TWO")
    check_return['nb_three'] *= G.GET("H_SELECT_THREE")
    check_return['nb_free_three'] *= G.GET("H_SELECT_FREE_THREE")
    check_return['nb_free_four'] *= G.GET("H_SELECT_FREE_FOUR")
    check_return['nb_four'] *= G.GET("H_SELECT_FOUR")
    check_return['nb_win'] *= G.GET("H_SELECT_WIN")
    check_return['nb_vulnerable'] *= G.GET("H_SELECT_VULNERABLILITY")
    check_return['nb_destroyed'] *= G.GET("H_SELECT_DESTROYED")

    val = 0
    for k in check_return:
        val += check_return[k]
    return val


@get_stats
def get_heuristic(node, printDebug=False):
    val = selective_heuristic(node, printDebug=printDebug)

    node.heuristic = val
    return val
