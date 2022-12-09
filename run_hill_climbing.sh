export ROW_SHAPE=250
export COL_SHAPE=300
export SIMULATIONS=1000

python algorithms/hill_climbing.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-simulations=$SIMULATIONS