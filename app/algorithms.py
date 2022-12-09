import numpy as np
import time
import math

from utils import (
    get_first_id_row_first,
    get_first_id_row_col,
    choose_best_move,
    negative_line_ids,
    choose_random,
    all_line_ids,
    generate_random_states,
    k_best_moves,
    apply_best_moves,
    find_k_best_board_ids
)

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

        if chosen_id['line'] == 'row':
            next_board = table.get_row_changed(chosen_id['id'])
        else:
            next_board = table.get_col_changed(chosen_id['id'])

        table.board = next_board

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

def first_choice_hill_climbing(table, choose_function):

    if choose_function=='row_first':
        choose_function = get_first_id_row_first
    elif choose_function=='row_col':
        choose_function = get_first_id_row_col

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

        current_temp = init_temperature / float(num_iter + 1)


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