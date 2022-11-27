export ROW_SHAPE=40
export COL_SHAPE=50
export K=3

python algorithms/k-beams.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-k=$K
