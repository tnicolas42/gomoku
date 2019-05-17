from random import randrange

s = 6
board = [0] * s

def getRow(board, x, y):
    return (board[y] & (0b11 << x*2)) >> x*2

def setRow(board, x, y, val):
    board[y] = board[y] | (val << x*2)

# fill with random values
for y in range(len(board)):
    for x in range(s):
        val = randrange(0b100)
        setRow(board, x, y, val)
    print(format(board[y], '#0' + str(s*2 + 2) + 'b'))
    print('---')
print('---------')


for y in range(s):
    for x in range(s):
        nb = getRow(board, x, y)
        print(format(nb, '#04b'), end=' ')
    print()
