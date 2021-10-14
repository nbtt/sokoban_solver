from board import Board

from time import time
from copy import deepcopy
from myqueue import MyQueue
from queue import PriorityQueue

import heapq

'''
Executes breadth-first search
uses MyQueue to keep track of frontier
'''

class Sokoban:

    '''
    Sokoban game class
    '''

    def __init__(self):
        self.nodes_newstate = 0
        self.explored = set()

    def new_board(self, filename):
        ''' Creates new board from file '''
        e = []  # empty solution list
        b = Board(e)
        with open(filename, 'r') as f:  # automatically closes file
            read_data = f.read()
            lines = read_data.split('\n')
            height = lines.pop(0)
            x = 0
            y = 0
            for line in lines:
                for char in line:
                    # adds Spots to board's sets by reading in char
                    if char == '@':
                        b.add_wall(x, y)
                    elif char == 'o':
                        b.add_goal(x, y)
                    elif char == 'i':
                        b.set_player(x, y)
                    elif char == '$':
                        # player gets its own Spot marker
                        b.set_player(x, y)
                        b.add_goal(x, y)
                    elif char == '+':
                        b.add_box(x, y)
                    elif char == '*':
                        b.add_box(x, y)
                        b.add_goal(x, y)
                    x += 1
                y += 1
                x = 0
            # check for a board with no player
            if hasattr(b, 'player'):
                return b
            else:
                print ("No player on board")
                return None

    # nodes_newstate = 0
    # explored = set()
    # Node NewState
    def numNodeNewState(self):
        return self.nodes_newstate
    # Explored
    def numNodeExplored(self):
        return self.explored
    #BFS
    def BFS_search(self, board):
        self.nodes_newstate = 0
        #nodes_newstate = 0
        if board.is_win():
            return board
        node = deepcopy(board) 
        self.nodes_newstate += 1
        frontier = MyQueue()
        frontier.push(node)
        self.explored = set()
        #explored = set() #nut kham pha
        keepLooking = True
        while keepLooking:
            if frontier.isEmpty():
                print ("Solution not found")
                return
            else:
                currNode = frontier.pop()
                moves = currNode.moves_available()
                currNode.fboxes = frozenset(currNode.boxes)
                self.explored.add(currNode)
                for m in moves:
                    child = deepcopy(currNode)
                    self.nodes_newstate += 1
                    child.move(m)
                    if child not in self.explored:
                        if child.is_win():
                            return child
                        frontier.push(child)
    # A star Search
    def aStar_search(self, board):
        self.nodes_newstate = 0
        #nodes_newstate = 0
        if board.is_win():
            return board
        initState = deepcopy(board) 
        self.nodes_newstate += 1
        heuQueue = PriorityQueue()
        heuQueue.put(initState)
        self.explored = set()
        #explored = set()
        keepLooking = True 
        while keepLooking:
            if heuQueue.empty():
                print ("Solution not found")
                return
            else:
                currNode = heuQueue.get()
                moves = currNode.moves_available()
                currNode.fboxes = frozenset(currNode.boxes)
                self.explored.add(currNode)
                for m in moves:
                    child = deepcopy(currNode)
                    self.nodes_newstate += 1
                    child.move(m)
                    if child not in self.explored:
                        if child.is_win():
                            return child
                        heuQueue.put(child)
                
    # NEW
    def a_star_new(self, board):
        if board.is_win():
            return board
        node = deepcopy(board)
        frontier = []
        frontierSet = set()
        heapq.heappush(frontier, node)
        frontierSet.add(node)
        explored = set()
        keepLooking = True
        while keepLooking:
            if len(frontier) == 0:
                print ("Solution not found")
                return
            else:
                currNode = heapq.heappop(frontier)
                frontierSet.remove(currNode)
                if currNode.is_win():
                    return currNode
                moves = currNode.moves_available()
                currNode.fboxes = frozenset(currNode.boxes)
                explored.add(currNode)
                for m in moves:
                    child = deepcopy(currNode)
                    child.move(m)
                    if child.is_win():
                        return child
                    if child not in explored:
                        if child not in frontierSet:
                            heapq.heappush(frontier, child)
                            frontierSet.add(child)
                    elif child in frontierSet:
                        count = frontier.count(child)
                        i = 0
                        while i <= count:
                            a = frontier.pop((frontier.index(child)))
                            if child.cost < a.cost:
                                heapq.heappush(frontier, child)
                                child = a
                                i = count + 1
                            else:
                                heapq.heappush(frontier, a)
                                i += 1
