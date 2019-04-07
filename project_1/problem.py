from search import Problem
from grid import *


class RobotRouteProblem(Problem):
    """The problem of moving the robot from a specific coordinate (x,y) at the grid to another"""
    def __init__(self, initial, goal, grid):
        Problem.__init__(self, initial, goal)
        self.grid = grid

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
