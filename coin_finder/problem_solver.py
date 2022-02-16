import copy
import sys
import os

import maze
import coin_problem

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import breadth_first_graph_search

if __name__ == "__main__":
    state = maze.Maze(5)
    state.build_maze()
    state.add_walls(4)
    coin_location = state.add_coin()

    goal = copy.deepcopy(state)
    goal.map[coin_location[0]][coin_location[1]] = 0
    goal.map[0][0] = -8

    print("Start state:")
    state.print_maze()
    print("\nGoal state:")
    goal.print_maze()

    # problem = coin_problem.CoinProblem(state, goal)
    # while not problem.goal_test(state):
    #     breadth_first_graph_search(problem)
    #     state.print_maze()
    #     print("\n")
