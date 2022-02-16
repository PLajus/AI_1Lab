import sys
import os

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

    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)


    def actions(self, state):
        """Isrenka tolimesnius galimus veiksmus."""

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

        if state.location[0] == 0 and state.location[1] == 0:
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
        elif state.location[0] == state.size and state.location[1] == 0:
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')
        elif state.location[0] == 0 and state.location[1] == state.size:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
        elif state.location[0] == state.size and state.location[1] == state.size:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')

        for action in possible_actions:
            if action == 'UP':
                if state.map[state.location[0] + 1][state.location[1]] == -1:
                    possible_actions.remove("UP")
            if action == 'DOWN':
                if state.map[state.location[0] - 1][state.location[1]] == -1:
                    possible_actions.remove("DOWN")
            if action == 'RIGHT':
                if state.map[state.location[0]][state.location[1] + 1] == -1:
                    possible_actions.remove("RIGHT")
            if action == 'LEFT':
                if state.map[state.location[0]][state.location[1] - 1] == -1:
                    possible_actions.remove("LEFT")

        if not possible_actions:
            raise ValueError("Goal is unreachable! Please generate a new map.")

        return possible_actions

    def result(self, state, action):
        """Grazina nauja busena atlikus veiksma duotoje busenoje."""

        state.map[state.location[0]][state.location[1]] = state.current_value

        if action == 'UP': 
            state.location[0] += 1
        elif action == 'DOWN':
            state.location[0] -= 1
        elif action == 'LEFT':
            state.location[1] -= 1
        elif action == 'RIGHT':
            state.location[1] += 1

        state.current_value = state.map[state.location[0]][state.location[1]]
        state.map[state.location[0]][state.location[1]] = 0

        return state

    def value(self, state):
        pass
