import logging
import random
from typing import List


class GameOfLife:
    def __init__(self, size):
        self._generate_random_table(size)

    @property
    def table(self):
        return self._table

    def _generate_random_table(self, size) -> List[List[int]]:
        logging.debug("creating empty table")

        table = [[0 for _ in range(size)] for _ in range(size)]  # blank table
        self._table = table

        rand = random.Random()
        first_point_count = rand.randint(50, 150)

        logging.debug("start position table contains %d active points" % first_point_count)

        for _ in range(first_point_count):
            row = rand.randint(0, size - 1)
            col = rand.randint(0, size - 1)

            table[row][col] = 1
            table[self._get_correct_index(row + 1)][col] = 1
            table[row][self._get_correct_index(col + 1)] = 1

        self._table = table

    def _get_correct_index(self, index: int):
        return index % len(self._table)

    def _get_neighbours_cells(self, prev_gen, row, col):
        check_row = (-1, -1, 0, 1, 1, 1, 0, -1)
        check_col = (0, -1, -1, -1, 0, 1, 1, 1)

        check_list = zip(check_col, check_row)

        ans = []

        for coordinates in check_list:
            add_to_col, add_to_row = coordinates
            correct_row = self._get_correct_index(row + add_to_row)
            correct_col = self._get_correct_index(col + add_to_col)
            ans.append(prev_gen[correct_row][correct_col])

        return ans

    def __next__(self):
        prev_generation = self.table.copy()

        for row in range(len(prev_generation)):
            for col in range(len(prev_generation[row])):
                current_cell = prev_generation[row][col]

                neighbors_sum = sum(self._get_neighbours_cells(prev_generation, row, col))

                if neighbors_sum == 3:  # create life
                    self.table[row][col] = 1
                elif current_cell and neighbors_sum == 2 or neighbors_sum == 3:  # let cell alive
                    self.table[row][col] = 1
                else:
                    self.table[row][col] = 0  # destroy life

        return self
