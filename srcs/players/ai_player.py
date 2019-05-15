import time
import math
import heapq
import random
from srcs.heuristic import get_heuristic
from srcs.players.player import Player
from srcs.players.Node import Node
from srcs.utils.stats import *
from srcs.const import *

class MaxHeapObj(object):
    def __init__(self,val): self.val = val
    def __lt__(self,other): return self.val > other.val
    def __eq__(self,other): return self.val == other.val
    def __str__(self): return str(self.val)
    def __repr__(self): return self.val.__repr__()

class AIPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)
        self.type_ = "AI"

    @set_marker(aftertxt="")
    @get_stats_and_mark()
    def move(self):
        """
        this function is called when the AI need to move
        -> put a stone on the board
        """
        if G.DEBUG_KEEP_NODE_PERCENT or G.DEBUG_ANTICIPATION:
            self.game.board.reset_debug()
        # put the first stone in the middle
        if (self.game.board.remain_places == G.GET("BOARD_SZ") * G.GET("BOARD_SZ")):
            self.game.board.put_stone(int(G.GET("BOARD_SZ") / 2), int(G.GET("BOARD_SZ") / 2), self.stone)
        else:
            transpositionTable = {}
            depth = min(G.GET("DEPTH"), self.game.board.remain_places)
            nodes = Node(self.game, transpositionTable, not self.stone, -1, -1, depth+1, None)
            move = min_max(nodes, depth)
            if move is None:
                return None
            node = move['node']
            tmp_depth = depth - 1
            while node.parent.parent:
                if G.DEBUG_ANTICIPATION:
                    self.game.board.content_desc[node.y][node.x]['debug_txt'] = (str(tmp_depth), STONES[node.board.content[node.y][node.x]])
                    tmp_depth -= 1
                node = node.parent
            self.game.board.put_stone(node.x, node.y, self.stone)

def heuristic(node):
    res = get_heuristic(node)
    return res

def is_terminal_node(node):
    node.setChilds()
    return len(node.childs) == 0

def min_max(node, depth, maximize=True, alpha=float('-inf'), beta=float('inf')):
    """
    min_max algorithm implementation
    """
    if node.game.reset_game:
        return None
    if depth == 0 or is_terminal_node(node):
        return {'node': node, 'cost': heuristic(node)}
    if maximize:
        _max = float('-inf')
        maxlst = None
        if G.GET("ENABLE_KEEP_NODE_PERCENT"):
            keepChilds = []
            for child in node.childs:
                heuristic(child)
                if child.heuristic is not None:
                    if depth == G.GET("DEPTH") and child.is_win:
                        return {'node': child, 'cost': heuristic(node)}
                    heapq.heappush(keepChilds, MaxHeapObj(child))
            range_ = max(math.ceil(len(keepChilds) * G.GET("KEEP_NODE_PERCENT")), G.GET("MIN_KEEP_NODE"))
            if G.GET("USE_MAX_KEEP_NODE"):
                range_ = min(range_, G.GET("MAX_KEEP_NODE"))
            range_ = range(range_)
        else:
            range_ = node.childs

        for i in range_:
            if G.GET("ENABLE_KEEP_NODE_PERCENT"):
                child = keepChilds[i].val
            else:
                child = i
            if G.DEBUG_KEEP_NODE_PERCENT and depth == G.GET("DEPTH"):
                node.game.board.content_desc[child.y][child.x]['debug_marker_color'] = STONES[child.stone]

            childMin = min_max(child, depth-1, False, alpha, beta)
            if childMin is None:
                return None
            if childMin['cost'] is None:
                continue
            if childMin['cost'] > _max:
                _max = childMin['cost']
                maxlst = [childMin['node']]
            elif childMin['cost'] == _max:
                maxlst.append(childMin['node'])
            alpha = max(alpha, _max)
            if beta <= alpha:
                break
        if maxlst is None:
            return {'node': None, 'cost': None}
        if G.MINMAX_RANDOM_CHOICE:
            _node = random.choice(maxlst)
        else:
            _node = maxlst[0]
        return {'node': _node, 'cost': _max}
    else:
        _min = float('inf')
        minlst = None
        if G.GET("ENABLE_KEEP_NODE_PERCENT"):
            keepChilds = []
            for child in node.childs:
                heuristic(child)
                if child.heuristic is not None:
                    heapq.heappush(keepChilds, child)
            range_ = max(math.ceil(len(keepChilds) * G.GET("KEEP_NODE_PERCENT")), G.GET("MIN_KEEP_NODE"))
            if G.GET("USE_MAX_KEEP_NODE"):
                range_ = min(range_, G.GET("MAX_KEEP_NODE"))
            range_ = range(range_)
        else:
            range_ = node.childs

        for i in range_:
            if G.GET("ENABLE_KEEP_NODE_PERCENT"):
                child = keepChilds[i]
            else:
                child = i

            childMax = min_max(child, depth-1, True, alpha, beta)
            if childMax is None:
                return None
            if childMax['cost'] is None:
                continue
            if childMax['cost'] < _min:
                _min = childMax['cost']
                minlst = [childMax['node']]
            elif childMax['cost'] == _min:
                minlst.append(childMax['node'])
            beta = min(beta, _min)
            if beta <= alpha:
                break
        if minlst is None:
            return {'node': None, 'cost': None}
        if G.MINMAX_RANDOM_CHOICE:
            _node = random.choice(minlst)
        else:
            _node = minlst[0]
        return {'node': _node, 'cost': _min}
