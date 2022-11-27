import numpy as np

from table import Table

def generate_random_states(table,k,p):
    table_class_lst = np.append(np.array([table]), ([Table(table.row_shape, table.col_shape) for _ in range(k-1)]), axis=0)
    for i in range(1,k):
        table_class_lst[i].set_board(table.board)
        table_class_lst[i].randomize_board_signs(p=p)
    return table_class_lst


def best_moves(table, k):
    row_best, col_best = [], []
    row_sums, col_sums = table.line_sums
    line_sums = np.append(row_sums, col_sums)
    for _ in range(k):
        min_id = np.argmin(line_sums)
        if min_id<table.row_shape:
            row_best.append(min_id)
        else:
            col_best.append(min_id-table.row_shape)
        line_sums[min_id] = float('inf')
    return row_best, col_best

def apply_best_moves(table, best_tuple):
    row_best, col_best = best_tuple
    best_table_list = np.empty(shape=(len(row_best)+len(col_best),table.row_shape,table.col_shape))
    for i in range(len(row_best)):
        best_table_list[i] = table.get_row_changed(row_best[i])
    for i in range(len(col_best)):
        best_table_list[i+len(row_best)] = table.get_col_changed(col_best[i])
    return best_table_list

def find_best_board_ids(board_list, k):
    util_list = np.array([np.sum(i) for i in board_list])
    maxlist = []
    for _ in range(k):
        cur_best_id = np.argmax(util_list)
        maxlist.append(cur_best_id)
        util_list[cur_best_id] = float('-inf')
    return maxlist