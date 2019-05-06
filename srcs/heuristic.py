from srcs.const import *


def _check_aligned_dir(game, tested_board, player_id, x, y, stone, addx, addy, check_return):
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
            if tested_board[new_y - addy][new_x - addx]['stone'] == STONE_EMPTY:
                free_side[0] = True
            break
        # if player stone
        elif tested_board[new_y][new_x]['stone'] == stone:
            nb_almost_aligned += 1
            if nb_hole[0] == 0:
                nb_aligned += 1
        # if empty
        elif tested_board[new_y][new_x]['stone'] == STONE_EMPTY:
            if tested_board[new_y - addy][new_x - addx]['stone'] == stone:
                if nb_hole[0] == 0:
                    nb_hole[0] = 1
                else:
                    free_side[0] = True
                    break
            elif tested_board[new_y - addy][new_x - addx]['stone'] == STONE_EMPTY:
                nb_hole[0] = 0
                free_side[0] = True
                break
        # if other stone
        else:
            if tested_board[new_y - addy][new_x - addx]['stone'] == STONE_EMPTY:
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
            if tested_board[new_y + addy][new_x + addx]['stone'] == STONE_EMPTY:
                free_side[0] = True
            break
        # if player stone
        elif tested_board[new_y][new_x]['stone'] == stone:
            nb_almost_aligned += 1
            if nb_hole[1] == 0:
                nb_aligned += 1
        # if empty
        elif tested_board[new_y][new_x]['stone'] == STONE_EMPTY:
            if tested_board[new_y + addy][new_x + addx]['stone'] == stone:
                if nb_hole[1] == 0:
                    nb_hole[1] = 1
                else:
                    free_side[1] = True
                    break
            elif tested_board[new_y + addy][new_x + addx]['stone'] == STONE_EMPTY:
                nb_hole[1] = 0
                free_side[1] = True
                break
        # if other stone
        else:
            if tested_board[new_y + addy][new_x + addx]['stone'] == STONE_EMPTY:
                nb_hole[1] = 0
                free_side[1] = True
            break
        new_x -= addx
        new_y -= addy

    if nb_aligned >= NB_ALIGNED_VICTORY:  # AAAAA
        check_return['nb_win'] += 1 if player_id == stone else -1
    elif nb_aligned >= 4:
        if free_side[0] + free_side[1] == 2:  # .AAAA.
            check_return['nb_free_four'] += 1 if player_id == stone else -1
        elif free_side[0] + free_side[1] == 1:  # BAAAA.
            check_return['nb_four'] += 1 if player_id == stone else -1
    elif nb_almost_aligned >= 4:  # AA.AA  AAA.AA
        check_return['nb_four'] += 1 if player_id == stone else -1
    elif nb_almost_aligned == 3:
        if free_side[0] + free_side[1] == 2:  # .A.AA.  .AAA.
            check_return['nb_free_three'] += 1 if player_id == stone else -1


def _check_vulnerability(game, tested_board, player_id, x, y, stone, check_return):
    """
    check the vulnerability of one stone
    """
    if stone == STONE_EMPTY:
        return False
    # for 4 stones: abcd with b is x y -> a=x1y1 b=xy c=x2y2 d=x3y3
    vul_cond = lambda x1, y1, x2, y2, x3, y3: (
                    0 <= x1 < game.board.size and 0 <= x2 < game.board.size and 0 <= x3 < game.board.size and
                    0 <= y1 < game.board.size and 0 <= y2 < game.board.size and 0 <= y3 < game.board.size and
                    tested_board[y][x]['stone'] == tested_board[y2][x2]['stone'] and
                    tested_board[y1][x1]['stone'] != stone and tested_board[y3][x3]['stone'] != stone and
                    tested_board[y1][x1]['stone'] != tested_board[y3][x3]['stone'] and
                    (tested_board[y1][x1]['stone'] == STONE_EMPTY or tested_board[y3][x3]['stone'] == STONE_EMPTY))
    vul_tab = (
        (x-1, y, x+1, y, x+2, y),
        (x+1, y, x-1, y, x-2, y),
        (x, y-1, x, y+1, x, y+2),
        (x, y+1, x, y-1, x, y-2),
        (x-1, y-1, x+1, y+1, x+2, y+2),
        (x-1, y+1, x+1, y-1, x+2, y-2),
        (x+1, y-1, x-1, y+1, x-2, y+2),
        (x+1, y+1, x-1, y-1, x-2, y-2),
    )
    for vul_tab_i in vul_tab:
        if vul_cond(*vul_tab_i):
            tested_board[y][x]['vulnerability'] = True
            check_return['nb_vulnerable'] += 1 if player_id == stone else -1
            return True
    tested_board[y][x]['vulnerability'] = False
    return False


def _check_stone(game, tested_board, player_id, x, y, check_return):
    """
    on the stone, check ->
        the nb of free three
        the nb of free four
        the nb of win
        the number of vulnerability
    """
    stone = tested_board[y][x]['stone']
    if stone == STONE_EMPTY:
        return

    _check_vulnerability(game, tested_board, player_id, x, y, stone, check_return)

    _check_aligned_dir(game, tested_board, player_id, x, y, stone, -1, 0, check_return)
    _check_aligned_dir(game, tested_board, player_id, x, y, stone, 0, 1, check_return)
    _check_aligned_dir(game, tested_board, player_id, x, y, stone, 1, 1, check_return)
    _check_aligned_dir(game, tested_board, player_id, x, y, stone, 1, -1, check_return)


H_BASIC_FREE_THREE = 30  # .AAA. .A.AA.
H_BASIC_FREE_FOUR = 40  # .AAAA.
H_BASIC_FOUR = 30  # BAAAA. AA.AA
H_BASIC_WIN = 50  # AAAAA
H_BASIC_VULNERABLILITY = -5  # BAA.

def basic_heuristic(game, tested_board, player_id):
    """
    :param game: the Game object (self.game)
    :param tested_board: this is the board to test
    :param player_id: this is the id of the actual player (self.game.id_player_act)
    """
    check_return = dict(
        nb_free_three=0,
        nb_free_four=0,
        nb_four=0,
        nb_win=0,
        nb_vulnerable=0,
    )
    for x in range(game.board.size):
        for y in range(game.board.size):
            _check_stone(game, tested_board, player_id, x, y, check_return)

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


    heuristic = 0
    for k in check_return:
        heuristic += check_return[k]
    return heuristic