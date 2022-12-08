import argparse
import numpy as np
import time
import pandas as pd
import shutil
import os

from table import Table
from utils import get_first_id_row_first
from utils import get_first_id_row_col

parser = argparse.ArgumentParser()
parser.add_argument('-row_shape', type=int, help='number of rows of the table')
parser.add_argument('-col_shape', type=int, help='number of columns of the table')
parser.add_argument('-choose_function', type=str, help='the function to choose the negative line')
parser.add_argument('-exper_num', type=int, help='the number of times to perform the experiment')
parser.add_argument('-results_dir', type=str, help='directory to save the results')
args = parser.parse_args()


if args.choose_function=='row_first':
    choose_function = get_first_id_row_first
elif args.choose_function=='row_col':
    choose_function = get_first_id_row_col
else:
    raise Exception('Please input a valid choosing function')


def first_choice_hill_climbing(table):
    num_iter = 0
    start = time.time()
    while True:
        if table.if_goal:
            abstime = time.time() - start
            return {'solution utility':np.sum(table.get_utility), 
                'number of iterations': num_iter, 
                'time': abstime}
        num_iter +=1
        change_id = choose_function(table=table)
        if change_id['line']=='row':
            table.set_board(table.get_row_changed(change_id['id']))
        else:
            table.set_board(table.get_col_changed(change_id['id']))

results = {'utility': [], 'niter': [], 'time': []}

for iter in range(args.exper_num):
    tb = Table(row_shape=args.row_shape, col_shape=args.col_shape)
    tb.create_table()
    tmp_results = first_choice_hill_climbing(tb)
    
    results['utility'].append(tmp_results['solution utility'])
    results['niter'].append(tmp_results['number of iterations'])
    results['time'].append(tmp_results['time'])

exper_dir = f'results/first_choice/{args.results_dir}'

if os.path.isdir(exper_dir):
    shutil.rmtree(exper_dir)

resdf = pd.DataFrame(results)
resdf.to_csv(exper_dir)