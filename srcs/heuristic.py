from srcs.utils.stats import get_stats
from srcs.const import *


def _check_aligned_dir(game, node, x, y, stone, addx, addy, check_return):
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
        check_return['nb_win'] += 1 if game.id_player_act == stone else -1
    elif nb_aligned >= 4:
        if free_side[0] + free_side[1] == 2:  # .AAAA.
            check_return['nb_free_four'] += 1 if game.id_player_act == stone else -1
        elif free_side[0] + free_side[1] == 1:  # BAAAA.
            check_return['nb_four'] += 1 if game.id_player_act == stone else -1
    elif nb_almost_aligned >= 4:  # AA.AA  AAA.AA
        check_return['nb_four'] += 1 if game.id_player_act == stone else -1
    elif nb_almost_aligned == 3:
        if free_side[0] + free_side[1] == 2:  # .A.AA.  .AAA.
            check_return['nb_free_three'] += 1 if game.id_player_act == stone else -1

def _check_stone(game, node, x, y, check_return):
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
        check_return['nb_vulnerable'] += 1 if game.id_player_act == stone else -1
    _check_aligned_dir(game, node, x, y, stone, -1, 0, check_return)
    _check_aligned_dir(game, node, x, y, stone, 0, 1, check_return)
    _check_aligned_dir(game, node, x, y, stone, 1, 1, check_return)
    _check_aligned_dir(game, node, x, y, stone, 1, -1, check_return)

    nb_destroyed = node.board.check_destroyable(x, y, stone)
    if len(nb_destroyed) > 0:
        check_return['nb_destroyed'] += len(nb_destroyed) * (1 if game.id_player_act == stone else -1)


H_BASIC_FREE_THREE = 50  # .AAA. .A.AA.
H_BASIC_FREE_FOUR = 100  # .AAAA.
H_BASIC_FOUR = 30  # BAAAA. AA.AA
H_BASIC_WIN = 200  # AAAAA
H_BASIC_VULNERABLILITY = -10  # BAA.
H_BASIC_DESTROYED = 30  # ABBA -> A..A

@get_stats
def basic_heuristic(node):
    """
    :param game: the Game object (self.game)
    :param tested_board: this is the board to test
    :param player_id: this is the id of the actual player (self.game.id_player_act)
    """
    game = node.game
    check_return = dict(
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
    check_return['nb_free_three'] /= 3
    check_return['nb_four'] /= 4
    check_return['nb_free_four'] /= 4
    check_return['nb_win'] /= 5

    # print(end="nb_free_three: %d " % (check_return['nb_free_three']))
    # print(end="nb_four: %d " % (check_return['nb_four']))
    # print(end="nb_free_four: %d " % (check_return['nb_free_four']))
    # print(end="nb_win: %d " % (check_return['nb_win']))
    # print("nb_vulnerable: %d " % (check_return['nb_vulnerable']))

    # apply a value
    check_return['nb_free_three'] *= H_BASIC_FREE_THREE
    check_return['nb_free_four'] *= H_BASIC_FREE_FOUR
    check_return['nb_four'] *= H_BASIC_FOUR
    check_return['nb_win'] *= H_BASIC_WIN
    check_return['nb_vulnerable'] *= H_BASIC_VULNERABLILITY
    check_return['nb_destroyed'] *= H_BASIC_DESTROYED


    heuristic = 0
    for k in check_return:
        heuristic += check_return[k]
    return heuristic