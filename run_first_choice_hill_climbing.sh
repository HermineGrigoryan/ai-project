export ROW_SHAPE=250
export COL_SHAPE=300
export CHOOSE_FUNTION=row_first
export EXPER_NUM=1000
export RESULTS_DIR=hc_250_300.csv

python algorithms/first_choice_hill_climbing.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-choose_function=$CHOOSE_FUNTION \
-exper_num=$EXPER_NUM \
-results_dir=$RESULTS_DIR