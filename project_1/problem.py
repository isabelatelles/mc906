from search import Problem
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt


class Grid:
    """
    Square matrix (2-dimensional array) of order n
    The matrix is composed by the follow data:
    1 (where there's a wall which the robot can't pass through) or
    0 (where there's no wall and the robot can walk) or
    2 (where the robot has passed through)
    The origin of the matrix, coordinate (0, 0) is the top-left corner
    """
    def __init__(self, order, walls_fraction=(1.0/3, 2.0/3)):
        """
        Set the data of the matrix, according to the order and the walls fraction
        Given the default value of the walls fraction, the order of the matrix should be a multiple of 3
        :param order: number of rows and columns of the matrix
        :param walls_fraction: tuple of fractions (x, y) of the grid that the middle walls will occupy
        """
        self.order = order
        self.walls_fraction = walls_fraction
        self.data = np.pad(np.zeros((self.order - 2, self.order - 2)), 1, mode='constant', constant_values=1)
        # Set data of left wall
        self.data[self.order - int(self.walls_fraction[1] * self.order):, int(self.walls_fraction[0] * self.order)] = \
            np.ones(int(self.walls_fraction[1] * self.order))
        # Set data of right wall
        self.data[0:int(self.walls_fraction[1] * self.order), self.order - int(self.walls_fraction[0] * self.order)] = \
            np.ones(int(self.walls_fraction[1] * self.order))

    def __getitem__(self, item):
        y, x = item
        return self.data[y][x]

    def __setitem__(self, key, value):
        self.data[key[0]][key[1]] = value

    def get_order(self):
        return self.order

    def plot(self):
        plt.imshow(self.data, interpolation='nearest')
        plt.show()


class RobotPosition:
    """
    Robot position in the grid, as well as the information if there are walls or not in the positions around
    """
    def __init__(self, x=None, y=None, direction=None, walls=None):
        """
        :param x: coordinate x
        :param y: coordinate y
        :param direction: angle of action that resulted in this position
        :param walls: list of booleans representing walls at adjacent positions at the follow angles
        0 degrees, 45 degrees, 90 degrees, 135 degrees, 180 degrees, 225 degrees, 270 degrees, 315 degrees
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.walls = walls

    def __eq__(self, other):
        if other.x == self.x and other.y == self.y:
            return True
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def get_location(self):
        return self.x, self.y

    def get_direction(self):
        return self.direction

    def get_walls(self):
        return self.walls

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def set_direction(self, direction):
        self.direction = direction

    def set_walls(self, grid):
        self.walls = list()
        self.walls.append(True if grid[self.y, self.x + 1] == 1 else False)
        self.walls.append(True if grid[self.y - 1, self.x + 1] == 1 else False)
        self.walls.append(True if grid[self.y - 1, self.x] == 1 else False)
        self.walls.append(True if grid[self.y - 1, self.x - 1] == 1 else False)
        self.walls.append(True if grid[self.y, self.x - 1] == 1 else False)
        self.walls.append(True if grid[self.y + 1, self.x - 1] == 1 else False)
        self.walls.append(True if grid[self.y + 1, self.x] == 1 else False)
        self.walls.append(True if grid[self.y + 1, self.x + 1] == 1 else False)


class RobotRouteProblem(Problem):
    """The problem of moving the robot from a specific coordinate (x,y) at the grid to another"""
    def __init__(self, initial, goal, grid):
        Problem.__init__(self, initial, goal)
        self.grid = grid

    def __str__(self):
        return 'RobotRouteProblem(' + str(self.grid.get_order()) + ', ' + str(self.initial) + ', ' + str(self.goal) + ')'

    def actions(self, state):
        """The actions of a position at a grid are its neighbors, given by each angle used to reach each neighbor"""
        possible_actions = [0, 45, 90, 135, 180, 225, 270, 315]
        direction = state.get_direction()
        walls = state.get_walls()

        angle = 0
        for i in range(8):
            if walls[i] is True and angle in possible_actions:
                possible_actions.remove(angle)
            angle += 45

        if direction == 0 and 180 in possible_actions:
            possible_actions.remove(180)
        elif direction == 45 and 225 in possible_actions:
            possible_actions.remove(225)
        elif direction == 90 and 270 in possible_actions:
            possible_actions.remove(270)
        elif direction == 135 and 315 in possible_actions:
            possible_actions.remove(315)
        elif direction == 180 and 0 in possible_actions:
            possible_actions.remove(0)
        elif direction == 225 and 45 in possible_actions:
            possible_actions.remove(45)
        elif direction == 270 and 90 in possible_actions:
            possible_actions.remove(90)
        elif direction == 315 and 135 in possible_actions:
            possible_actions.remove(135)

        return possible_actions

    def result(self, state, action):
        """The result of each action is given by adding or subtracting the coordinates (x, y)"""
        new_state = RobotPosition()
        x, y = state.get_location()

        if action == 0:
            new_state.set_location(x + 1, y)
            new_state.set_direction(0)
        elif action == 45:
            new_state.set_location(x + 1, y - 1)
            new_state.set_direction(45)
        elif action == 90:
            new_state.set_location(x, y - 1)
            new_state.set_direction(90)
        elif action == 135:
            new_state.set_location(x - 1, y - 1)
            new_state.set_direction(135)
        elif action == 180:
            new_state.set_location(x - 1, y)
            new_state.set_direction(180)
        elif action == 225:
            new_state.set_location(x - 1, y + 1)
            new_state.set_direction(225)
        elif action == 270:
            new_state.set_location(x, y + 1)
            new_state.set_direction(270)
        elif action == 315:
            new_state.set_location(x + 1, y + 1)
            new_state.set_direction(315)

        new_state.set_walls(self.grid)

        return new_state

    def manhattan(self, node):
        x, y = node.state.get_location()
        x_goal, y_goal = self.goal.get_location()

        return abs(x_goal - x) + abs(y_goal - y)

    def euclidean(self, node):
        x, y = node.state.get_location()
        x_goal, y_goal = self.goal.get_location()

        return sqrt((x_goal - x)**2 + (y_goal - y)**2)
