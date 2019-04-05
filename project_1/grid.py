import numpy as np
import matplotlib.pyplot as plt


class Grid:
    """
    Square matrix (2-dimensional array) of order n
    The matrix is composed by the follow data:
    1 (where there's a wall which the robot can't pass through) or 0 (where there's no wall and the robot can walk)
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
        print()

    def plot(self):
        plt.imshow(self.data, interpolation='nearest')
        plt.show()
