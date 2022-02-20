"""
2022-02-17
Povilas Lajus
Ernest Petrovic
Mindaugas Gaidys
"""

import sys
import os

from items import Item

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import Problem

class CoinProblem(Problem):
        
    """
    NxN labirintas, kuriame reikia pasiekti langeli su moneta, pazymeta ($).
    Pajudejimas i langeli kainuoja taskus, kuriu verte yra sugeneruota atsitikinai.
    Labirinte yra sienos, pazymetos (#). I siuos langelius eiti negalima. 
    Sienos generuojamos atsitiktinai.
    Tikslas - pasiekti moneta.
    """

    def __init__(self, initial, goal=None, maze=None):
        """Konstruktorius"""

        self.initial = initial
        self.goal = goal
        self.maze = maze

    def actions(self, state):
        """Isrenka tolimesnius galimus veiksmus."""

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

        # Tikrina ar neiseis is ribu
        if state[1] == 0:
            possible_actions.remove('UP')
        if state[1] == self.maze.size - 1:
            possible_actions.remove('DOWN')
        if state[2] == 0:
            possible_actions.remove('LEFT')
        if state[2] == self.maze.size - 1:
            possible_actions.remove('RIGHT')

        # Tikrina ar neeis i siena
        for action in possible_actions:
            if action == 'UP':
                if self.maze.map[state[1] - 1][state[2]] == Item.WALL:
                    possible_actions.remove("UP")
            if action == 'DOWN':
                if self.maze.map[state[1] + 1][state[2]] == Item.WALL:
                    possible_actions.remove("DOWN")
            if action == 'RIGHT':
                if self.maze.map[state[1]][state[2] + 1] == Item.WALL:
                    possible_actions.remove("RIGHT")
            if action == 'LEFT':
                if self.maze.map[state[1]][state[2] - 1] == Item.WALL:
                    possible_actions.remove("LEFT")

        if not possible_actions:
            raise ValueError("Goal is unreachable! Please generate a new maze.")

        return possible_actions

    def result(self, state, action):
        """Grazina nauja busena atlikus veiksma duotoje busenoje."""
        
        new_state = list(state)

        if action == 'UP':
            new_state[1] -= 1
        elif action == 'DOWN':
            new_state[1] += 1
        elif action == 'LEFT':
            new_state[2] -= 1
        elif action == 'RIGHT':
            new_state[2] += 1

        new_state[0] = self.maze.map[new_state[1]][new_state[2]]

        return tuple(new_state)

    def value(self, state):
        """Busenos verte optimizavimo algoritmams"""

        return state[0]

    def path_cost(self, c, state1, action, state2):
        """Apskaiciuoja kelio kaina"""

        return c + state1[0]
