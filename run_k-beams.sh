export ROW_SHAPE=250
export COL_SHAPE=300
export K=3
export P=0.5
export EXPER_NUM=1000
export RESULTS_DIR=beams_250_300.csv

python algorithms/k-beams.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-k=$K \
-p=$P \
-exper_num=$EXPER_NUM \
-results_dir=$RESULTS_DIR
