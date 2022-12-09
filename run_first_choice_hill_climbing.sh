export ROW_SHAPE=250
export COL_SHAPE=300
export CHOOSE_FUNTION=row_first
export SIMULATIONS=1000

python algorithms/first_choice_hill_climbing.py \
-row_shape=$ROW_SHAPE \
-col_shape=$COL_SHAPE \
-choose_function=$CHOOSE_FUNTION \
-simulations=$SIMULATIONS