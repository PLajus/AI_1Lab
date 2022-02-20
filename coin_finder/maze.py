"""
2022-02-17
Povilas Lajus
Ernest Petrovic
Mindaugas Gaidys
"""

import random
from items import Item

class Maze:

    """"
    Klase atsakinga uz labirinto sukurima ir atvaizdavima.
    """

    def __init__(self, size) -> None:
        self.size = size
        self.map = {y: {x: 0 for x in range(size)} for y in range(size)}

    def build_maze(self):
        """Suraso langeliu vertes"""

        for row in range(self.size):
            for col in range(self.size):
                val = random.randrange(1,10)
                self.map[row][col] = val
        self.map[0][0] = 0

    def add_coin(self):
        """Ideda moneta (goal)"""

        row = random.randrange(1, self.size)
        col = random.randrange(1, self.size)
        self.map[row][col] = Item.COIN
        return [row, col]


    def add_walls(self, num_of_walls):
        """Sudeda sienas"""

        for wall in range(num_of_walls):
            row = random.randrange(1, self.size)
            col = random.randrange(1, self.size)
            self.map[row][col] = Item.WALL

    def print_maze(self, current_x, current_y):
        """Atspausdina labirinta"""

        for row in range(self.size):
            for col in range(0, self.size):
                if self.map[row][col] == Item.WALL:
                    print("#", end= " ")
                elif self.map[row][col] == Item.COIN:
                    print("$", end= " ")
                elif row == current_x and col == current_y:
                    print("!", end=" ")
                else:
                    print(self.map[row][col], end= " ")
            print()
    print()
