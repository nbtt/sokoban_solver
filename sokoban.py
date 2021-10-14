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

    #BFS
    def search(self, board):
        if board.is_win():
            return board
        node = deepcopy(board) 
        frontier = MyQueue()
        frontier.push(node)
        explored = set() #nut kham pha
        keepLooking = True
        while keepLooking:
            if frontier.isEmpty():
                print ("Solution not found")
                return
            else:
                currNode = frontier.pop()
                moves = currNode.moves_available()
                currNode.fboxes = frozenset(currNode.boxes)
                explored.add(currNode)
                for m in moves:
                    child = deepcopy(currNode)
                    child.move(m)
                    if child not in explored:
                        if child.is_win():
                            return child
                        frontier.push(child)
    # A star Search
    def aStar_search(self, board):
        if board.is_win():
            return board
        initState = deepcopy(board) 
        heuQueue = PriorityQueue()
        heuQueue.put(initState)
        exploredQueue = set()
        keepLooking = True 
        while keepLooking:
            if heuQueue.empty():
                print ("Solution not found")
                return
            else:
                currNode = heuQueue.get()
                moves = currNode.moves_available()
                currNode.fboxes = frozenset(currNode.boxes)
                exploredQueue.add(currNode)
                for m in moves:
                    child = deepcopy(currNode)
                    child.move(m)
                    if child not in exploredQueue:
                        if not child.boxes.issubset(currNode.boxes):
                            if child.is_win():
                                return child
                        heuQueue.put(child)
