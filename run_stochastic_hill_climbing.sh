export ROW_SHAPE=250
export COL_SHAPE=300
export EXPER_NUM=1000
export RESULTS_DIR=stoch_250_300.csv

python algorithms/stochastic_hill_climbing.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-exper_num=$EXPER_NUM \
-results_dir=$RESULTS_DIR
