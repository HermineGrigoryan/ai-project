import argparse
import numpy as np
import time
import pandas as pd
from tqdm import tqdm

from table import Table
from utils import negative_line_ids, all_line_ids
from utils import choose_random


parser = argparse.ArgumentParser()
parser.add_argument('-row_shape', type=int, help='number of rows of the table')
parser.add_argument('-col_shape', type=int,
                    help='number of columns of the table')
parser.add_argument('-init_temperature', type=int, help='initial temperature')
parser.add_argument('-simulations', type=int, help='the number of simulations')
args = parser.parse_args()


def simulated_annealing(table, init_temperature):
    num_iter = 0
    current_temp = init_temperature
    start = time.time()
    while True:
        if table.if_goal:
            abstime = time.time() - start
            return {'solution utility': np.sum(table.get_utility),
                    'number of iterations': num_iter,
                    'time': abstime}

        num_iter += 1

        line_options = all_line_ids(table=table)
        chosen_id = choose_random(table=table, dct=line_options)

        if chosen_id['line'] == 'row':
            next_board = table.get_row_changed(chosen_id['id'])
        else:
            next_board = table.get_col_changed(chosen_id['id'])

        current_utility = table.get_utility
        next_utility = np.sum(next_board)

        delta_e = next_utility - current_utility
        metropolis = np.exp(-delta_e / current_temp)
        rand_prob = np.random.random()

        if delta_e > 0:
            table.board = next_board
        elif rand_prob < metropolis:
            table.board = next_board

        current_temp = current_temp / float(num_iter + 1)


results = {'utility': [], 'niter': [], 'time': []}

for iter in tqdm(range(args.simulations)):
    tb = Table(row_shape=args.row_shape, col_shape=args.col_shape)
    tb.create_table()
    tmp_results = simulated_annealing(tb, args.init_temperature)
    
    results['utility'].append(tmp_results['solution utility'])
    results['niter'].append(tmp_results['number of iterations'])
    results['time'].append(tmp_results['time'])


resdf = pd.DataFrame(results)
resdf.to_csv(f'results/simulated_annealing/simulated_annealing_{args.row_shape}_{args.col_shape}_{args.init_temperature}.csv', index=False)
