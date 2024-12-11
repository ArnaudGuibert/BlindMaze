# This Python file uses the following encoding: utf-8

from core import Maze, decompose_path
from solver import Solver

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic


class Window(QMainWindow):
    def __init__(self):
        # init components
        super(Window, self).__init__()
        uic.loadUi('window.ui', self)

        # connect events
        self.ui_buttonP1.clicked.connect(self.buttonP1_event)
        self.ui_buttonP2.clicked.connect(self.buttonP2_event)
        self.ui_buttonP3.clicked.connect(self.buttonP3_event)
        self.ui_label.paintEvent = self.label_event

        # attributes (starting with random maze)
        self.maze = Maze(16, full=True)
        self.maze.generate()
        self.solver = Solver()


    def reset_speed(self, straight = None, turns = None):
        # reset speed / counter lineedits
        if straight is None or turns is None:
            self.ui_lineedit_2.setText("")
            self.ui_lineedit_4.setText("")
            self.ui_lineedit_5.setText("")

        else:
            self.ui_lineedit_2.setText(str(straight))
            self.ui_lineedit_4.setText(str(turns))

            # compute full path time
            try:
                forw_time = float(self.ui_lineedit_1.text())
                turn_time = float(self.ui_lineedit_3.text())
                full_time = straight * forw_time + turns * turn_time
                self.ui_lineedit_5.setText(str(round(full_time, 1)))
            except Exception as e:
                print("Could not process time values entered in the UI")


    def buttonP1_event(self, event):
        # create new random maze
        self.maze = Maze(16, full=True)
        self.maze.generate()
        self.solver = Solver()

        self.reset_speed()
        self.ui_label.update()


    def buttonP2_event(self, event):
        # load saved maze from file
        self.maze = Maze.load('resources/japan_2017.pickle')
        self.solver = Solver()
        
        self.reset_speed()
        self.ui_label.update()


    def buttonP3_event(self, event):
        # create adequate solver
        if self.ui_buttonR1.isChecked():
            self.solver = Solver('random')
        elif self.ui_buttonR2.isChecked():
            self.solver = Solver('follower')
        elif self.ui_buttonR3.isChecked():
            self.solver = Solver('tremeaux')
        elif self.ui_buttonR4.isChecked():
            self.solver = Solver('floodfill')

        # fit to maze
        try:
            self.solver.fit(self.maze)
        except Exception as e:
            print(e)

        # update speed frame >> UI
        straight, turns = decompose_path(self.solver.real_path)
        self.reset_speed(straight, turns)
        self.ui_label.update()


    def label_event(self, event):
        # init painter
        qp = QPainter(self.ui_label)
        cs = 27 # cell size
        ms = self.maze.size * (cs - 1) + 1 # maze full size (with external walls)
        bd = (self.ui_label.width() - ms) // 2 # border (left and top)

        # draw both solver paths (if solved)
        if self.solver is not None:
            # real path
            real_path = set(self.solver.real_path)
            for tile in real_path:
                x1 = bd + (cs - 1) * tile[0]
                y1 = bd + (cs - 1) * tile[1]
                qp.fillRect(x1, y1, cs, cs, QColor(224, 255, 255))

            # optimal path
            qp.setPen(Qt.red)
            opti_path = self.solver.opti_path
            for curr, next in zip(opti_path, opti_path[1:]):
                x1 = bd + (cs - 1) * curr[0] + cs // 2
                y1 = bd + (cs - 1) * curr[1] + cs // 2
                x2 = bd + (cs - 1) * next[0] + cs // 2
                y2 = bd + (cs - 1) * next[1] + cs // 2
                qp.drawLine(x1, y1, x2, y2)
        
        # draw start tile
        x = bd + (cs - 1) * self.maze.start[0] + cs // 3
        y = bd + (cs - 1) * self.maze.start[1] + cs // 3
        qp.fillRect(x, y, cs // 3, cs // 3, Qt.red)

        # draw end tile
        x = bd + (cs - 1) * self.maze.end[0] + cs // 3
        y = bd + (cs - 1) * self.maze.end[1] + cs // 3
        qp.fillRect(x, y, cs // 3, cs // 3, Qt.blue)

        # draw maze walls
        qp.setPen(Qt.black)
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                cell = self.maze.grid[j][i]
                x1 = bd + (cs - 1) * cell.x
                y1 = bd + (cs - 1) * cell.y
                x2 = bd + (cs - 1) * cell.x + (cs - 1)
                y2 = bd + (cs - 1) * cell.y + (cs - 1)

                if cell.walls['W'] == 1:
                    qp.drawLine(x1, y1, x1, y2)
                if cell.walls['N'] == 1:
                    qp.drawLine(x1, y1, x2, y1)
                if cell.walls['E'] == 1:
                    qp.drawLine(x2, y1, x2, y2)
                if cell.walls['S'] == 1:
                    qp.drawLine(x1, y2, x2, y2)

