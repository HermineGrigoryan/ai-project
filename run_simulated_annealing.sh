export ROW_SHAPE=3
export COL_SHAPE=4
export INIT_TEMPERATURE=100
export SIMULATIONS=1000

python algorithms/simulated_annealing.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-init_temperature=$INIT_TEMPERATURE \
-simulations=$SIMULATIONS
