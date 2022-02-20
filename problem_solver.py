"""
2022-02-17
Povilas Lajus
Ernest Petrovic
Mindaugas Gaidys
"""

import sys
import os

import maze
import coin_problem

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import breadth_first_graph_search

if __name__ == "__main__":
    state = [0, 0, 0]
    
        #   val,x, y

    map = maze.Maze(5)
    map.build_maze()
    map.add_walls(3)
    coin_location = map.add_coin()

    goal = [-1, coin_location[0], coin_location[1]]

    print("Start:")
    map.print_maze(state[1], state[2])
    print()

    problem = coin_problem.CoinProblem(tuple(state), tuple(goal), map)

    solution = breadth_first_graph_search(problem).solution()
    print(solution)
    print(breadth_first_graph_search(problem).path()[-1].path_cost)
