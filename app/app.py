import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.express as px

from  table import Table
import algorithms as algo

st.set_page_config(page_title='AI Positive Table', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title('Positive Table')

st.sidebar.markdown("[![Foo](https://roost.ai/hs-fs/hubfs/logos/integrations/logo-github.png?width=100&height=100&name=logo-github.png)](https://github.com/HermineGrigoryan/ai-project)")
st.sidebar.markdown('# User Input Variables')
navigation = st.sidebar.radio('Navigation', ('Create a board', 'Simulations'))

import os
st.write(os.listdir())
st.write(os.listdir('results'))
st.write(os.listdir('results/hill_climbing'))

##################################
#### Quantitative Analysis #######
##################################

if navigation == 'Create a board':
    
    st.subheader('Project Details')
    '''
    Real numbers are written in an m×n table. 
    It is permissible to reverse the signs of all numbers in any row or column.
    Develop an AI that from a given board obtains a board, such that the sums of
     numbers along each line (row and column) are nonnegative.
    '''

    st.markdown('_'*100) # adding a breaking line
    st.subheader('Create a board')

    col1, col2, col3 = st.columns([1, 1, 0.5])
    row_shape = col1.slider('Row shape', 2, 100, 4, 2)
    col_shape = col2.slider('Column shape', 2, 100, 6, 2)
    fix_state = col3.checkbox('Fix the random state')
    if fix_state:
        random_state = col1.slider('Fix the random state to', value=42)
    else:
        random_state = None
    np.random.seed(random_state)
    tb = Table(row_shape=row_shape, col_shape=col_shape)
    tb.create_table()

    st.write('##### Initial board')
    st.dataframe(np.round(tb.board, 2))


    col1_algo, col2_algo, col3_algo = st.columns([1, 1, 1])
    solution_algo = col1_algo.selectbox('Solve the problem by using the following algorithm', 
                ['Hill climbing', 'Pseudo stochastic hill climbing', 
                'First-choice hill climbing', 'Simulated annealing', 'K-beams'])

    if solution_algo == 'Hill climbing':
        results = algo.hill_climbing(tb)

    if solution_algo == 'Pseudo stochastic hill climbing': 
        results = algo.stochastic_hill_climbing(tb)

    if solution_algo == 'First-choice hill climbing':
        choose_function = col2_algo.selectbox('Function', ['row_first', 'row_col'])
        results = algo.first_choice_hill_climbing(tb, choose_function)

    if solution_algo == 'Simulated annealing':
        init_temperature = col2_algo.slider('Initial temperature', 1, 100, 10, 10)
        results = algo.simulated_annealing(tb, init_temperature)

    if solution_algo == 'K-beams':
        k = col2_algo.slider('K', 2, 10, 3, 1)
        p = col3_algo.slider('P', 0.1, 1.0, 0.5, 0.1)
        results = algo.k_beams(tb, k, p)

    st.write('##### Solution of the board')
    st.dataframe(np.round(tb.board, 2))

    st.write('##### Statistics')
    st.write(pd.DataFrame.from_dict([results]))
    

##################################
####### Simulations    ###########
##################################
if navigation == 'Simulations':
    '''In this section, we present the simulation results using different local search algorithms.
    The number of simulations throughout this project is set to 10,000.
    Through simulations, we want to understand how each algorithm performs in regard to the number of
    moves needed for reaching the goal state for various row and column shapes of the board.
    The selected combinations of rows and columns are the following:                       
    $3×4, 45×50, 100×120, 250×300$'''

    board_size = st.radio('Board size', ['3×4', '45×50', '100×120', '250×300'], horizontal=True)
    row, col = board_size.split('×')

    st.header('Explore the performance of each algorithm separately')
    col1_algo, col2_algo, col3_algo = st.columns([1, 1, 1])
    solution_algo = col1_algo.selectbox('Simulation results for:', 
                ['Hill climbing', 'Pseudo stochastic hill climbing', 
                'First-choice hill climbing', 'Simulated annealing', 'K-beams'])

    try:
        if solution_algo == 'Hill climbing':
            st.write((f'results/hill_climbing/hill_climbing_{row}_{col}.csv'))
            data = pd.read_csv(f'results/hill_climbing/hill_climbing_{row}_{col}.csv')

        if solution_algo == 'Pseudo stochastic hill climbing':
            data = pd.read_csv(f'results/pseudo_stochastic_hill_climbing/pseudo_stochastic_hill_climbing_{row}_{col}.csv')

        if solution_algo == 'First-choice hill climbing':
            choose_function = col2_algo.selectbox('Function', ['row_first', 'row_col'])
            data = pd.read_csv(f'results/first_choice_hill_climbing/first_choice_hill_climbing_{row}_{col}_{choose_function}.csv')

        if solution_algo == 'Simulated annealing':
            init_temperature = col2_algo.radio('Initial temperature', [1, 10, 100], horizontal=True)
            data = pd.read_csv(f'results/simulated_annealing/simulated_annealing_{row}_{col}_{init_temperature}.csv')

        if solution_algo == 'K-beams':
            k = col2_algo.selectbox('K', [3])
            p = col3_algo.selectbox('P', [0.5])
            data = pd.read_csv(f'results/k_beams/k_beams_{row}_{col}_{k}_{p}.csv')

        profiling_table = data.describe().T
        st.write(profiling_table)
        selected_col = st.radio('Selected column', data.columns.tolist(), 1, horizontal=True)
        
        hist = px.histogram(data, selected_col)
        hist.add_vline(x=data[selected_col].mean(), line_width=2, line_dash="dash", line_color="black")
        st.plotly_chart(hist, use_container_width=True)
    
    except FileNotFoundError:
                st.warning(f'No file with such configurations was simulated!')

    st.header('Explore the performance of all algorithms')
    show_all = st.checkbox('Show the analysis')
    if show_all:
        '''Here we present simulation results for all algorithms with the following parameters:

        - Hill climbing
        
    - Pseudo stochastic hill climbing
        
    - First-choice hill climbing (row first)
        
    - Simulated annealing (initial temperature = 1)
        
    - K-beams (K=3)'''

        datasets = [f'hill_climbing_{row}_{col}',
                    f'pseudo_stochastic_hill_climbing_{row}_{col}',
                    f'first_choice_hill_climbing_{row}_{col}_row_first',
                    f'simulated_annealing_{row}_{col}_1',
                    f'k_beams_{row}_{col}_3_0.5']

        all_data = pd.DataFrame()

        for i in datasets:
            try:
                folder_name = re.findall(r'(\w+?)(\d+)', i)[0][0][:-1]
                tmp_df = pd.read_csv(f'results/{folder_name}/{i}.csv')
                tmp_df['algorithm'] = folder_name.replace('_', ' ').strip()
                all_data = pd.concat([all_data, tmp_df], ignore_index=True)
            except FileNotFoundError:
                st.warning(f'No `{i}` was simulated!')


        selected_col_all = st.radio('Selected column', ['utility', 'niter', 'time'], 1, horizontal=True, key='all')
        profiling_all = all_data[['algorithm', selected_col_all]].groupby('algorithm').describe()
        st.write(profiling_all)
        boxplot = px.box(all_data, x='algorithm', y=selected_col_all, color='algorithm')
        st.plotly_chart(boxplot, use_container_width=True)

        distplot = px.histogram(all_data, x=selected_col_all, color='algorithm', marginal='box', opacity=0.5)
        st.plotly_chart(distplot, use_container_width=True)