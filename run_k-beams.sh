export ROW_SHAPE=250
export COL_SHAPE=300
export K=3
export SIMULATIONS=1000

python algorithms/k-beams.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-k=$K \
-simulations=$SIMULATIONS
