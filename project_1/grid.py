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

    def __setitem__(self, key, value):
        self.data[key[0]][key[1]] = value

    def get_walls_around_position(self, x, y):
        walls = list()
        walls.append(True if self.data[y][x + 1] == 1 else False)
        walls.append(True if self.data[y - 1][x + 1] == 1 else False)
        walls.append(True if self.data[y - 1][x] == 1 else False)
        walls.append(True if self.data[y - 1][x - 1] == 1 else False)
        walls.append(True if self.data[y][x - 1] == 1 else False)
        walls.append(True if self.data[y + 1][x - 1] == 1 else False)
        walls.append(True if self.data[y + 1][x] == 1 else False)
        walls.append(True if self.data[y + 1][x + 1] == 1 else False)

        return walls

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

    def set_walls(self, walls):
        self.walls = walls
