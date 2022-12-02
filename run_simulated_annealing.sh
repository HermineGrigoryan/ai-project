export ROW_SHAPE=4
export COL_SHAPE=5
export INIT_TEMPERATURE=10

python algorithms/simulated_annealing.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-init_temperature=$INIT_TEMPERATURE
