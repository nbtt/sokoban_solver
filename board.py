from spot import Spot
from direction import Direction
from queue import Queue
L = Direction(Spot(-1, 0), 'l')
R = Direction(Spot(1, 0), 'r')
U = Direction(Spot(0, -1), 'u')
D = Direction(Spot(0, 1), 'd')
directions = [U, D, L, R]


class Board:
    def __init__(self, dir_list):
        self.dir_list = dir_list  
        self.walls = set()
        self.goals = set()
        self.boxes = set()
        self.fboxes = frozenset() 
        self.player = None
        self.cost = 1 
        self.heuristic = 0
        self.index = 0

    def __eq__(self, other):
        ''' checking for 'equality' of box positions and player positions '''
        if self.boxes.issubset(other.boxes) and self.player == other.player:
            return True
        else:
            return False

    def getHeuristic(self):
        box = list(self.boxes)
        goal = list(self.goals)
        numBox = len(box)
        sumG = 0
        for i in range(numBox):
            min = abs((box[i].x-goal[0].x)) + abs((box[i].y-goal[0].y))
            for j in range(1,numBox):
                temp = abs((box[i].x-goal[j].x)) + abs((box[i].y-goal[j].y))
                if (temp < min):
                    min = temp
            sumG += min
        sumP = sum(abs(box[i].x-self.player.x) + abs(box[i].y-self.player.y) for i in range(numBox))
        self.heuristic = sumG + sumP + numBox - len(self.boxes & self.goals)
        return self.heuristic

    def __hash__(self):
        ''' hashes by frozenset of box positions '''
        return hash((self.fboxes, self.player))

    def __gt__(self, other):
        ''' comparison by heuristic '''
        if self.getHeuristic() > other.getHeuristic():
            return True
        else:
            return False

    def __lt__(self, other):
        ''' comparison by heuristic '''
        if self.getHeuristic() < other.getHeuristic():
            return True
        else:
            return False

    def add_wall(self, x, y):
        self.walls.add(Spot(x, y))

    def add_goal(self, x, y):
        self.goals.add(Spot(x, y))

    def add_box(self, x, y):
        self.boxes.add(Spot(x, y))

    def set_player(self, x, y):
        self.player = Spot(x, y)

    def moves_available(self):
        ''' set newstate'''
        moves = []
        for d in directions:
            if self.player + d.sp not in self.walls:
                if self.player + d.sp in self.boxes:
                    if self.player + d.sp.double() not in self.boxes.union(self.walls):
                        moves.append(d)
                else:
                    moves.append(d)
        return moves

    def notfound(self):
        self.index = 1

    def move(self, direction):
        p = self.player + direction.sp
        if p in self.boxes:
            self.boxes.remove(p)
            self.boxes.add(p + direction.sp)
        self.player = p
        self.dir_list.append(direction)

    def is_win(self):
        ''' Checks for winning '''
        if self.goals.issubset(self.boxes):
            return True
        else:
            return False

    def getDirections(self):
        ''' contain solution '''
        if self.index != 0:
            return 'Not Found'
        chars = ''
        for d in self.dir_list:
            chars += d.char
        return chars