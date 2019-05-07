from srcs.utils.stats import get_stats
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
        if not (0 <= new_x < game.board.size and 0 <= new_y < game.board.size):
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
        if not (0 <= new_x < game.board.size and 0 <= new_y < game.board.size):
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

    if nb_aligned >= NB_ALIGNED_VICTORY:  # AAAAA
        check_return['nb_win'] += multiplier * (1 if game.id_player_act == stone else -1)
    elif nb_aligned >= 4:
        if free_side[0] + free_side[1] == 2:  # .AAAA.
            check_return['nb_free_four'] += multiplier * (1 if game.id_player_act == stone else -1)
        elif free_side[0] + free_side[1] == 1:  # BAAAA.
            check_return['nb_four'] += multiplier * (1 if game.id_player_act == stone else -1)
    elif nb_aligned >= 3:
        if free_side[0] + free_side[1] == 2:  # .AAA.
            check_return['nb_free_three'] += multiplier * (1 if game.id_player_act == stone else -1)
        elif free_side[0] + free_side[1] == 1:  # BAAA.
            check_return['nb_three'] += multiplier * (1 if game.id_player_act == stone else -1)
    elif nb_aligned >= 2:
        if free_side[0] + free_side[1] == 2:  # .AA.
            check_return['nb_free_two'] += multiplier * (1 if game.id_player_act == stone else -1)
        elif free_side[0] + free_side[1] == 1:  # BAA.
            check_return['nb_two'] += multiplier * (1 if game.id_player_act == stone else -1)
    elif nb_almost_aligned >= 4:  # AA.AA  AAA.AA
        check_return['nb_four'] += multiplier * (1 if game.id_player_act == stone else -1)
    elif nb_almost_aligned == 3:
        if free_side[0] + free_side[1] == 2:  # .A.AA.  .AAA.
            check_return['nb_free_three'] += multiplier * (1 if game.id_player_act == stone else -1)

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
        check_return['nb_vulnerable'] += multiplier * (1 if game.id_player_act == stone else -1)
    _check_aligned_dir(game, node, x, y, stone, -1, 0, check_return, multiplier=multiplier)
    _check_aligned_dir(game, node, x, y, stone, 0, 1, check_return, multiplier=multiplier)
    _check_aligned_dir(game, node, x, y, stone, 1, 1, check_return, multiplier=multiplier)
    _check_aligned_dir(game, node, x, y, stone, 1, -1, check_return, multiplier=multiplier)

    nb_destroyed = node.board.check_destroyable(x, y, stone)
    if len(nb_destroyed) > 0:
        check_return['nb_destroyed'] += multiplier * len(nb_destroyed) * (1 if game.id_player_act == stone else -1)


H_BASIC_TWO = 10  # .AA. BAA.
H_BASIC_THREE = 30  # BAAA.
H_BASIC_FREE_THREE = 80  # .AAA. .A.AA.
H_BASIC_FREE_FOUR = 300  # .AAAA.
H_BASIC_FOUR = 100  # BAAAA. AA.AA
H_BASIC_WIN = 1000  # AAAAA
H_BASIC_VULNERABLILITY = -10  # BAA.
H_BASIC_DESTROYED = 100  # ABBA -> A..A


def get_hash(node):
    return hash(str(node.board.content))


def basic_heuristic(node, printDebug=False):
    game = node.game

    hash_node = get_hash(node)
    if hash_node in node.transpositionTable:
        return node.transpositionTable[hash_node]

    check_return = dict(
        nb_three=0,
        nb_two=0,
        nb_free_three=0,
        nb_free_four=0,
        nb_four=0,
        nb_win=0,
        nb_vulnerable=0,
        nb_destroyed=0,
    )
    for x in range(game.board.size):
        for y in range(game.board.size):
            _check_stone(game, node, x, y, check_return)

    # a free three is calculated 3 times (for his 3 stones) so we need to divide it by 3
    # same thing for the others elements
    # !!! nb_vulnerable is the nmber of vulnerable pieces
    check_return['nb_two'] /= 2
    check_return['nb_three'] /= 3
    check_return['nb_free_three'] /= 3
    check_return['nb_four'] /= 4
    check_return['nb_free_four'] /= 4
    check_return['nb_win'] /= 5

    if printDebug:
        print(node.board)
        print(end="nb_two: %d " % (check_return['nb_two']))
        print(end="nb_three: %d " % (check_return['nb_three']))
        print(end="nb_free_three: %d " % (check_return['nb_free_three']))
        print(end="nb_four: %d " % (check_return['nb_four']))
        print(end="nb_free_four: %d " % (check_return['nb_free_four']))
        print(end="nb_destroyed: %d " % (check_return['nb_destroyed']))
        print(end="nb_vulnerable: %d " % (check_return['nb_vulnerable']))
        print(end="nb_win: %d " % (check_return['nb_win']))
        print()

    # apply a value
    check_return['nb_two'] *= H_BASIC_TWO
    check_return['nb_three'] *= H_BASIC_THREE
    check_return['nb_free_three'] *= H_BASIC_FREE_THREE
    check_return['nb_free_four'] *= H_BASIC_FREE_FOUR
    check_return['nb_four'] *= H_BASIC_FOUR
    check_return['nb_win'] *= H_BASIC_WIN
    check_return['nb_vulnerable'] *= H_BASIC_VULNERABLILITY
    check_return['nb_destroyed'] *= H_BASIC_DESTROYED

    val = 0
    for k in check_return:
        val += check_return[k]

    node.transpositionTable[hash_node] = val
    return val


H_SELECT_TWO = 10 // 2  # .AA. BAA.
H_SELECT_FREE_TWO = 15 // 2  # .AA. BAA.
H_SELECT_THREE = 30 // 3  # BAAA.
H_SELECT_FREE_THREE = 80 // 3  # .AAA. .A.AA.
H_SELECT_FREE_FOUR = 300 // 4  # .AAAA.
H_SELECT_FOUR = 100 // 4  # BAAAA. AA.AA
H_SELECT_WIN = 1000 // 5  # AAAAA
H_SELECT_VULNERABLILITY = -35  # BAA.
H_SELECT_DESTROYED = 90  # ABBA -> A..A


def selective_heuristic(node, printDebug=False):
    """
    calc the heuristic with particular attention with the ordered posed stones
    """
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
        tmp = tmp.parent

    for x, y, stone in node_hist:
        node.board.content[y][x] = STONE_EMPTY


    for x in range(game.board.size):
        for y in range(game.board.size):
            _check_stone(game, node, x, y, check_return)

    node_hist.reverse()
    lenhist = len(node_hist)
    for i, (x, y, stone) in enumerate(node_hist):
        node.board.put_stone(x, y, stone, test=True)
        _check_stone(game, node, x, y, check_return,
                     multiplier=((lenhist+1)>>1) - (i>>1))

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
    check_return['nb_two'] *= H_SELECT_TWO
    check_return['nb_free_two'] *= H_SELECT_FREE_TWO
    check_return['nb_three'] *= H_SELECT_THREE
    check_return['nb_free_three'] *= H_SELECT_FREE_THREE
    check_return['nb_free_four'] *= H_SELECT_FREE_FOUR
    check_return['nb_four'] *= H_SELECT_FOUR
    check_return['nb_win'] *= H_SELECT_WIN
    check_return['nb_vulnerable'] *= H_SELECT_VULNERABLILITY
    check_return['nb_destroyed'] *= H_SELECT_DESTROYED

    val = 0
    for k in check_return:
        val += check_return[k]
    return val


@get_stats
def get_heuristic(node, printDebug=False):
    # val = basic_heuristic(node, printDebug=printDebug)
    val = selective_heuristic(node, printDebug=printDebug)

    return val
