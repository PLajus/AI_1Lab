import random

class Maze:

    """"
    Klase atsakinga uz labirinto sukurima ir atvaizdavima.
    """

    def __init__(self, size) -> None:
        self.size = size
        self.map = {y: {x: 0 for x in range(size)} for y in range(size)}
        self.location = [0, 0]
        self.current_value = -8

    def __key(self):
        return (self.size, self.map, self.location, self.current_value)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Maze):
            return self.__key() == other.__key()
        return NotImplemented
        

    def build_maze(self):
        """Suraso langeliu vertes"""

        for row in range(self.size):
            for col in range(self.size):
                val = random.randrange(1,10)
                self.map[row][col] = val
        self.map[0][0] = -8

    def add_coin(self):
        """Ideda moneta (goal)"""

        row = random.randrange(1, self.size)
        col = random.randrange(1, self.size)
        self.map[row][col] = -1
        return [row, col]


    def add_walls(self, num_of_walls):
        """Sudeda sienas"""

        for i in range(num_of_walls):
            row = random.randrange(1, self.size)
            col = random.randrange(1, self.size)
            self.map[row][col] = -3

    def print_maze(self):
        """Atspausdina labirinta"""

        for row in range(self.size):
            for col in range(0, self.size):
                if self.map[row][col] == -3: # Siena
                    print("#", end= " ")
                elif self.map[row][col] == -1: # Moneta
                    print("$", end= " ")
                elif self.map[row][col] == 0: # Esama pozicija
                    print("!", end= " ")
                elif self.map[row][col] == -8: # Pradzios pozicija
                    print("S", end= " ")
                else:
                    print(self.map[row][col], end= " ")
            print()
    print()