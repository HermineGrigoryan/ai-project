import numpy as np

from table import Table


def generate_random_states(table, k, p):
    table_class_lst = np.append(np.array([table]), ([Table(
        table.row_shape, table.col_shape) for _ in range(k-1)]), axis=0)
    for i in range(1, k):
        table_class_lst[i].set_board(table.board)
        table_class_lst[i].randomize_board_signs(p=p)
    return table_class_lst


def k_best_moves(table, k):
    row_best, col_best = [], []
    row_sums, col_sums = table.line_sums
    line_sums = np.append(row_sums, col_sums)
    for _ in range(k):
        min_id = np.argmin(line_sums)
        if min_id < table.row_shape:
            row_best.append(min_id)
        else:
            col_best.append(min_id-table.row_shape)
        line_sums[min_id] = float('inf')
    return row_best, col_best


def apply_best_moves(table, best_tuple):
    row_best, col_best = best_tuple
    best_table_list = np.empty(
        shape=(len(row_best)+len(col_best), table.row_shape, table.col_shape))
    for i in range(len(row_best)):
        best_table_list[i] = table.get_row_changed(row_best[i])
    for i in range(len(col_best)):
        best_table_list[i+len(row_best)] = table.get_col_changed(col_best[i])
    return best_table_list


def find_k_best_board_ids(board_list, k):
    util_list = np.array([np.sum(i) for i in board_list])
    maxlist = []
    for _ in range(k):
        cur_best_id = np.argmax(util_list)
        maxlist.append(cur_best_id)
        util_list[cur_best_id] = float('-inf')
    return maxlist


def negative_line_ids(table):
    line_dct = {'row': [], 'col': []}
    for i in range(len(table.line_sums[0])):
        if table.line_sums[0][i] < 0:
            line_dct['row'].append(i)
    for i in range(len(table.line_sums[1])):
        if table.line_sums[1][i] < 0:
            line_dct['col'].append(i)
    line_dct['row'], line_dct['col'] = np.array(
        line_dct['row'], dtype=int), np.array(line_dct['col'], dtype=int)
    return line_dct


def all_line_ids(table):
    line_dct = {'row': [], 'col': []}
    for i in range(len(table.line_sums[0])):
        line_dct['row'].append(i)
    for i in range(len(table.line_sums[1])):
        line_dct['col'].append(i)
    line_dct['row'], line_dct['col'] = np.array(
        line_dct['row'], dtype=int), np.array(line_dct['col'], dtype=int)
    return line_dct


def choose_random(table, dct):
    row_lst, col_lst = dct.values()
    col_lst = col_lst+table.row_shape
    appended_lst = np.append(row_lst, col_lst, axis=0)
    if len(appended_lst) == 0:
        raise Exception('The passed list is empty')
    chosen_id = np.random.choice(appended_lst)
    line_type = 'row'
    if chosen_id >= table.row_shape:
        line_type = 'col'
        chosen_id = chosen_id-table.row_shape
    return {'line': line_type, 'id': chosen_id}


def choose_best_move(table):
    row_lst, col_lst = table.line_sums
    col_lst = col_lst+table.row_shape
    appended_lst = np.append(row_lst, col_lst, axis=0)
    chosen_id = np.argmin(appended_lst)
    line_type = 'row'
    if chosen_id >= table.row_shape:
        line_type = 'col'
        chosen_id = chosen_id - table.row_shape
    return {'line': line_type, 'id': chosen_id}


def get_first_id_row_first(table):
    row_sign_lst = np.sign(table.line_sums[0])
    min_row_id = np.argmin(row_sign_lst)
    if row_sign_lst[min_row_id] < 0:
        return {'line': 'row', 'id': min_row_id}
    return {'line': 'col', 'id': np.argmin(np.sign(table.line_sums[1]))}


def get_first_id_row_col(table):
    row_sign_lst = np.sign(table.line_sums[0])
    col_sign_lst = np.sign(table.line_sums[1])
    min_row_id = np.argmin(row_sign_lst)
    min_col_id = np.argmin(col_sign_lst)
    if min_col_id < min_row_id:
        if col_sign_lst[min_col_id] < 0:
            return {'line': 'col', 'id': min_col_id}
    elif row_sign_lst[min_row_id] >= 0:
        return {'line': 'col', 'id': min_col_id}
    return {'line': 'row', 'id': min_row_id}
