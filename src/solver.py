# This Python file uses the following encoding: utf-8

import random as rd
from collections import Counter
from core import Maze


class Solver:
    def __init__(self, solvertype='random'):
        # init variables
        self.solvertype = solvertype
        self.real_path = []
        self.opti_path = []


    def fit(self, maze):
        if self.solvertype == 'random':
            self.fit_random(maze)
        
        elif self.solvertype == 'follower':
            self.fit_follower(maze)
        
        elif self.solvertype == 'tremeaux':
            self.fit_tremeaux(maze)
        
        elif self.solvertype == 'floodfill':
            self.fit_floodfill(maze)


    def fit_random(self, maze):
        # init
        self.real_path = [ maze.start ]
        gfou = 0

        while maze.end not in self.real_path:
            # garde-fou (nombre iterations)
            gfou += 1
            if gfou == 30000:
                raise Exception("Method ended: reached max. number of iterations")

            x, y = self.real_path[-1]
            neigh = maze.get_open_neighbors(x, y)

            # pick-a-cell
            p = rd.randint(0, len(neigh) - 1)
            nx, ny = neigh[p]
            self.real_path += [ (nx, ny) ]
        
        # set optimal path by detecting multiple tile crossing
        opti_path = self.real_path.copy()
        c = [ a for (a,b) in Counter(opti_path).items() if b > 1 ]

        while len(c) > 0:
            indices = [ i for i, a in enumerate(opti_path) if a == c[0] ]
            idx1, idx2 = indices[0], indices[-1]
            new_path = opti_path[:idx1+1] + opti_path[idx2+1:]
            opti_path = new_path.copy()
            c = [ a for (a,b) in Counter(opti_path).items() if b > 1 ]
        
        self.opti_path = opti_path


    def fit_follower(self, maze):
        # init (hand to left wall)
        self.real_path = [ maze.start ]
        direct, order = 'E', [ 'N', 'E', 'S', 'W' ]
        gfou = False

        while maze.end not in self.real_path:
            # garde-fou (boucle infinie)
            if gfou:
                if self.real_path[-1] == self.real_path[1]:
                    raise Exception("Method failed: stuck in a loop")
            else:
                gfou = len(self.real_path) != 1 and self.real_path[-1] == maze.start

            x, y = self.real_path[-1]
            cell = maze.grid[y][x]

            # pick-a-cell
            idx_start = order.index(direct) - 1
            for i in range(4):
                idx = (idx_start + i) % 4
                direct = order[idx]
                if cell.walls[direct] == 0:
                    nx, ny = maze.get_neighbor(x, y, direct)
                    self.real_path += [ (nx, ny) ]
                    break
        
        # set optimal path by detecting multiple tile crossing
        opti_path = self.real_path.copy()
        c = [ a for (a,b) in Counter(opti_path).items() if b > 1 ]

        while len(c) > 0:
            indices = [ i for i, a in enumerate(opti_path) if a == c[0] ]
            idx1, idx2 = indices[0], indices[-1]
            new_path = opti_path[:idx1+1] + opti_path[idx2+1:]
            opti_path = new_path.copy()
            c = [ a for (a,b) in Counter(opti_path).items() if b > 1 ]
        
        self.opti_path = opti_path


    def fit_tremeaux(self, maze):
        # init / stone pellets are stored in an intersection dictionary with keys (x_min,x_max,y_min,y_max)
        # for example, the intersection between Cell(x=2, y=5) and Cell(x=2, y=4) is key=(2,2,4,5)
        self.real_path = [ maze.start ]
        intersect = {}
        for i in range(maze.size):
            for j in range(maze.size-1):
                intersect[(i,i,j,j+1)] = 0
                intersect[(j,j+1,i,i)] = 0

        while maze.end not in self.real_path:
            x, y = self.real_path[-1]
            neigh = maze.get_open_neighbors(x, y)
            pellets = [ intersect[(min(x,a),max(x,a),min(y,b),max(y,b))] for (a,b) in neigh ]

            # rule 1 (initial rule)
            if len(self.real_path) == 1:
                choice = [ ne for (ne, pel) in zip(neigh, pellets) if pel == 0 ]
                p = rd.randint(0, len(choice) - 1)
                nx, ny = choice[p]

            else:
                px, py = self.real_path[-2]
                # rule 1 (only entrance intersection is marked)
                if 0 in pellets and sum(pellets) == intersect[(min(x,px),max(x,px),min(y,py),max(y,py))]:
                    choice = [ ne for (ne, pel) in zip(neigh, pellets) if pel == 0 ]
                    p = rd.randint(0, len(choice) - 1)
                    nx, ny = choice[p]
                
                # rule 2 (going back if possible)
                elif intersect[(min(x,px),max(x,px),min(y,py),max(y,py))] == 1:
                    nx, ny = px, py
                
                # rule 3 (pick the entrance with the fewest marks possible)
                else:
                    pel_min = min(pellets)
                    choice = [ ne for (ne, pel) in zip(neigh, pellets) if pel == pel_min ]
                    p = rd.randint(0, len(choice) - 1)
                    nx, ny = choice[p]

            # update nb of pellets on intersection
            intersect[(min(x,nx),max(x,nx),min(y,ny),max(y,ny))] += 1
            self.real_path += [ (nx, ny) ]

        # set optimal path using (stone pellets == 1)
        opti_path = [ maze.start ]
        while maze.end not in opti_path:
            x, y = opti_path[-1]
            neigh = [ (a,b) for (a,b) in maze.get_open_neighbors(x, y) if (a,b) not in opti_path ]
            pellets = [ intersect[(min(x,a),max(x,a),min(y,b),max(y,b))] for (a,b) in neigh ]
            opti_path += [ neigh[pellets.index(1)] ]
        
        self.opti_path = opti_path


    def fit_floodfill(self, maze):
        # init distance maze
        maze_dist = Maze(maze.size, start=maze.start, end=maze.end, full=False)
        maze_dist.flood()

        # create path (start -> end)
        self.real_path = [ maze.start ]
        order = [ 'W', 'S', 'N', 'E' ]

        while maze.end not in self.real_path:
            x, y = self.real_path[-1]
            cell = maze.grid[y][x]

            # go forward if you decrease your cost
            progress = False
            for dir in order:
                if cell.walls[dir] == 0:
                    nx, ny = maze.get_neighbor(x, y, dir)
                    if maze_dist.grid[ny][nx].dist == maze_dist.grid[y][x].dist - 1:
                        self.real_path += [ (nx, ny) ]
                        progress = True
                        break
            
            # update walls and flood if you are stuck
            if not progress:
                for (x,y) in set(self.real_path):
                    cell = maze.grid[y][x]
                    for dir in order:
                        if cell.walls[dir] == 1:
                            maze_dist.set_wall(x, y, dir, wall=1)
                maze_dist.flood()

        # set optimal path using distance to exit
        opti_path = [ maze.start ]
        
        maze_dist = Maze(maze.size, start=maze.start, end=maze.end, full=True)
        for (x,y) in set(self.real_path):
            cell = maze.grid[y][x]
            for dir in order:
                if cell.walls[dir] == 0:
                    maze_dist.set_wall(x, y, dir, wall=0)
        maze_dist.flood()

        while maze.end not in opti_path:
            x, y = opti_path[-1]
            value = maze_dist.grid[y][x].dist
            for (a,b) in maze_dist.get_open_neighbors(x, y):
                if (a,b) in self.real_path and maze_dist.grid[b][a].dist == value - 1:
                    opti_path += [ (a,b) ]
                    break
        
        self.opti_path = opti_path

