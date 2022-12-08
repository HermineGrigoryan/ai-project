import argparse
import numpy as np
import time
import pandas as pd
import os
import shutil

from table import Table
from utils import choose_best_move, negative_line_ids


parser = argparse.ArgumentParser()
parser.add_argument('-row_shape', type=int, help='number of rows of the table')
parser.add_argument('-col_shape', type=int, help='number of columns of the table')
parser.add_argument('-exper_num', type=int, help='the number of times to perform the experiment')
parser.add_argument('-results_dir', type=str, help='directory to save the results')
args = parser.parse_args()


def hill_climbing(table):
    num_iter = 0
    start = time.time()
    while True:
        if table.if_goal:
            abstime = time.time() - start
            return {'solution utility': table.get_utility,
                    'number of iterations': num_iter,
                    'time': abstime}
        num_iter += 1
        chosen_id = choose_best_move(table)
        if chosen_id['line'] == 'row':
            table.set_board(table.get_row_changed(chosen_id['id']))
        else:
            table.set_board(table.get_col_changed(chosen_id['id']))

results = {'utility': [], 'niter': [], 'time': []}

for iter in range(args.exper_num):
    tb = Table(row_shape=args.row_shape, col_shape=args.col_shape)
    tb.create_table()
    tmp_results = hill_climbing(tb)
    
    results['utility'].append(tmp_results['solution utility'])
    results['niter'].append(tmp_results['number of iterations'])
    results['time'].append(tmp_results['time'])

exper_dir = f'results/hill_climbing/{args.results_dir}'

if os.path.isdir(exper_dir):
    shutil.rmtree(exper_dir)

resdf = pd.DataFrame(results)
resdf.to_csv(exper_dir)
