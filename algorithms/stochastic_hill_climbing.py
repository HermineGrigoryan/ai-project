import argparse
import numpy as np
import time
import pandas as pd
from tqdm import tqdm

from table import Table
from utils import negative_line_ids
from utils import choose_random


parser = argparse.ArgumentParser()
parser.add_argument('-row_shape', type=int, help='number of rows of the table')
parser.add_argument('-col_shape', type=int, help='number of columns of the table')
parser.add_argument('-simulations', type=int, help='the number of simulations')
args = parser.parse_args()


def stochastic_hill_climbing(table):
    num_iter = 0
    start = time.time()
    while True:
        if table.if_goal:
            abstime = time.time() - start
            return {'solution utility':np.sum(table.get_utility), 
                'number of iterations': num_iter, 
                'time': abstime}
        num_iter +=1
        line_options = negative_line_ids(table=table)
        chosen_id = choose_random(table=table, dct=line_options)
        if chosen_id['line']=='row':
            table.set_board(table.get_row_changed(chosen_id['id']))
        else:
            table.set_board(table.get_col_changed(chosen_id['id']))

results = {'utility': [], 'niter': [], 'time': []}

for iter in tqdm(range(args.simulations)):
    tb = Table(row_shape=args.row_shape, col_shape=args.col_shape)
    tb.create_table()
    tmp_results = stochastic_hill_climbing(tb)
    
    results['utility'].append(tmp_results['solution utility'])
    results['niter'].append(tmp_results['number of iterations'])
    results['time'].append(tmp_results['time'])


resdf = pd.DataFrame(results)
resdf.to_csv(f'results/stochastic_hill_climbing/stochastic_hill_climbing_{args.row_shape}_{args.col_shape}.csv', index=False)