from srcs.const import *

def _at(board, x, y):
    '''
        Return the content at the board given position
    '''
    return (board[y] & (0b11 << (x<<1))) >> (x<<1)

def _set(board, x, y, val):
    '''
        Set the content of the board given position
    '''
    # clear the position
    board[y] = board[y] & (((1 << (G.GET("BOARD_SZ")<<1))-1) ^ (0b11 << (x<<1)))
    # fill the position
    board[y] = board[y] | (val << (x<<1))
