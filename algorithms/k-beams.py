import numpy as np
import argparse
import time
import math
import pandas as pd
from tqdm import tqdm

from table import Table
from utils import generate_random_states
from utils import k_best_moves
from utils import apply_best_moves
from utils import find_k_best_board_ids

parser = argparse.ArgumentParser()
parser.add_argument('-row_shape', type=int, help='number of rows of the table')
parser.add_argument('-col_shape', type=int, help='number of columns of the table')
parser.add_argument('-k', type=int, help='parameter k in k-beams algorithm')
parser.add_argument('-simulations', type=int, help='the number of simulations')
args = parser.parse_args()

tb = Table(row_shape=args.row_shape, col_shape=args.col_shape)
tb.create_table()

def k_beams(table, k, p):
    num_iter = 0
    start = time.time()
    table_class_list = generate_random_states(table=table, k=k, p=p)
    
    for i in range(k):
        if table_class_list[i].if_goal:
            abstime = time.time() - start
            return {'solution utility':np.sum(table_class_list[i].board), 
                'number of iterations': num_iter, 
                'time': abstime}
    while True:
        num_iter += 1
        best_move_list = [k_best_moves(table=i, k=k) for i in table_class_list]
        best_list = np.array([apply_best_moves(table_class_list[math.floor(i/k)],best_move_list[math.floor(i/k)])[i%k] for i in range(k*k)])
        selected_board_ids = find_k_best_board_ids(best_list,k)
        for i in range(k):
            table_class_list[i].set_board(best_list[selected_board_ids[i]])
            if table_class_list[i].if_goal:
                abstime = time.time() - start
                return {'solution utility':np.sum(table_class_list[i].board), 
                'number of iterations': num_iter, 
                'time': abstime}

p = 0.5
results = {'utility': [], 'niter': [], 'time': []}

for iter in tqdm(range(args.simulations)):
    tb = Table(row_shape=args.row_shape, col_shape=args.col_shape)
    tb.create_table()
    tmp_results = k_beams(table=tb, k=args.k, p=p)
    
    results['utility'].append(tmp_results['solution utility'])
    results['niter'].append(tmp_results['number of iterations'])
    results['time'].append(tmp_results['time'])


resdf = pd.DataFrame(results)
resdf.to_csv(f'results/k_beams/k_beams_{args.row_shape}_{args.col_shape}_{args.k}_{p}.csv', index=False)