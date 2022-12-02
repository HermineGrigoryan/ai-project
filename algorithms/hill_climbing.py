import argparse
import numpy as np
import time

from table import Table
from utils import choose_best_move, negative_line_ids


parser = argparse.ArgumentParser()
parser.add_argument('-row_shape', type=int, help='number of rows of the table')
parser.add_argument('-col_shape', type=int,
                    help='number of columns of the table')
args = parser.parse_args()


def hill_climbing(table):
    num_iter = 0
    start = time.time()
    while True:
        if table.if_goal:
            abstime = time.time() - start
            return {'solution utility': np.sum(table.get_utility),
                    'number of iterations': num_iter,
                    'time': abstime}

        num_iter += 1
        chosen_id = choose_best_move(table)
        # print(table.board)
        # print(table.line_sums)
        # print(chosen_id)

        if chosen_id['line'] == 'row':
            next_board = table.get_row_changed(chosen_id['id'])
        else:
            next_board = table.get_col_changed(chosen_id['id'])

        current_utility = table.get_utility
        next_utility = np.sum(next_board)
        if current_utility > next_utility:
            print('Only local maximum was reached')
            break

        if next_utility > current_utility:
            table.board = next_board


for i in range(100):
    tb = Table(row_shape=args.row_shape, col_shape=args.col_shape)
    tb.create_table()
    print(hill_climbing(tb))
