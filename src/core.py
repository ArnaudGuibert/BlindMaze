# This Python file uses the following encoding: utf-8

import random as rd
import pickle


class Cell:
    def __init__(self, x, y, wall = 1):
        self.x = x
        self.y = y
        self.walls = { 'W' : wall, 'N' : wall, 'E' : wall, 'S' : wall }
        self.dist = 0


    def connect(self, cell):
        # break walls
        if self.x - cell.x == 1:
            self.walls['W'] = 0
            cell.walls['E'] = 0
        elif self.x - cell.x == -1:
            self.walls['E'] = 0
            cell.walls['W'] = 0
        elif self.y - cell.y == 1:
            self.walls['N'] = 0
            cell.walls['S'] = 0
        else:
            self.walls['S'] = 0
            cell.walls['N'] = 0



class Maze:
    def __init__(self, size=16, start=None, end=None, full=True):
        # params
        self.start = start if start is not None else (0, 0)
        self.end = end if end is not None else (size-1, size-1)
        
        # grid of cells
        self.size = size
        
        # fully dense maze
        if full:
            self.grid = [ [ Cell(i, j, wall=1) for i in range(self.size) ] for j in range(self.size) ]
        
        # empty maze with ext. borders
        else:
            grid = [ [ Cell(i, j, wall=0) for i in range(self.size) ] for j in range(self.size) ]
            for i in range(self.size):
                grid[0][i].walls['N'] = 1
                grid[i][0].walls['W'] = 1
                grid[self.size-1][i].walls['S'] = 1
                grid[i][self.size-1].walls['E'] = 1
            self.grid = grid


    def get_neighbors(self, x, y):
        adjacent = [ (x+a, y+b) for (a,b) in [ (-1, 0), (1, 0), (0, -1), (0, 1) ] ]
        return [ (a,b) for (a,b) in adjacent if 0 <= a <= self.size - 1 and 0 <= b <= self.size - 1 ]
    

    def get_open_neighbors(self, x, y):
        towards = { 'N' : (0,-1) , 'E' : (1,0) , 'S' : (0,1) , 'W' : (-1,0) }
        neigh = [ (x+a, y+b) for dir, (a,b) in towards.items() if self.grid[y][x].walls[dir] == 0 ]
        return neigh


    def get_neighbor(self, x, y, dir):
        towards = { 'N' : (0,-1) , 'E' : (1,0) , 'S' : (0,1) , 'W' : (-1,0) }
        a, b = towards[dir]
        return (x+a, y+b)
    

    def set_wall(self, x, y, dir, wall=1):
        # get adjacent cell if available and add wall(s)
        oppo = { 'N' : 'S', 'S' : 'N', 'E' : 'W', 'W' : 'E' }
        nx, ny = self.get_neighbor(x, y, dir)

        self.grid[y][x].walls[dir] = wall
        if 0 <= nx <= self.size - 1 and 0 <= ny <= self.size - 1:
            self.grid[ny][nx].walls[oppo[dir]] = wall
    

    def generate(self):
        # init Aldous-Broder algorithm to create a perfect maze
        x, y = self.size // 2, self.size // 2
        visited, stack = [ (x,y) ], [ (x,y) ]

        # loop
        while len(visited) < self.size ** 2:
            x, y = stack[-1][0], stack[-1][1]
            neigh = [ val for val in self.get_neighbors(x, y) if val not in visited ]

            if neigh == []:
                stack.pop()
            else:
                p = rd.randint(0, len(neigh) - 1)
                nx, ny = neigh[p][0], neigh[p][1]

                self.grid[y][x].connect(self.grid[ny][nx])
                visited += [ (nx,ny) ]
                stack += [ (nx,ny) ]


    def save(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self, f, protocol = pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print("Error with pickle:", e)
    

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            maze = pickle.load(f)
        return maze
    

    def flood(self):
        # flood function for the "floodfill" solver
        x, y = self.end
        self.grid[y][x].dist = 0
        visited = [ (x, y) ]

        # build border
        border = []
        for (x,y) in visited:
            neigh = self.get_open_neighbors(x, y)
            border += [ (a,b) for (a,b) in neigh if (a,b) not in visited ]

        # loop
        counter = 0
        while border != []:
            # update distance
            counter += 1
            for (x,y) in border:
                self.grid[y][x].dist = counter
            visited += border

            # rebuild border
            border = []
            for (x,y) in visited:
                neigh = self.get_open_neighbors(x, y)
                border += [ (a,b) for (a,b) in neigh if (a,b) not in visited and (a,b) not in border ]



def decompose_path(path):
    # init
    forward, turns = 0, 0
    dx, dy = None, None

    for curr, next in zip(path, path[1:]):
        x1, y1 = curr[0], curr[1]
        x2, y2 = next[0], next[1]

        dx_new = x2 - x1
        dy_new = y2 - y1

        forward += 1
        if dx is not None:
            comp = 1 - (dx_new * dx + dy_new * dy)
            turns += comp

        dx = dx_new
        dy = dy_new

    # forward / turns
    return forward, turns

