# AI Project - Positive Table
This repository contains codes for AI course. The problem statement of this project is the following:

Real numbers are written in an m×n table. It is permissible to reverse the signs of all numbers in any row or column.  Develop an AI that from a given    board obtains a board, such that the sums of numbers along each line (row and column) are nonnegative.

In order to solve this proble, various local search algorithms were applied, such as hill climbing, pseudo-stochastic hill climbing, first-choice hill climbing, simulated annealing and k-beams. The experiments are conducted using $3×4, 45×50, 100×120, 250×300$ tables generated using $N ~ (0,20)$ random normal distribution. 10,000 simulations are conducted for $3×4, 45×50, 100×120$ boards, and 1,000 simulations for $250×300$ board. 

The codes are organized in the following manner:

The root directory contains **algorithms**, **app**, **results**.

The **algorithms** folder contains the following files:
- The implementations of local search algorithms
- The class of the table (e.g., table creation, calculation of the line sums, change of line number signs, etc.)
- General utility functions used in the implementation of all the algorithms

The **app** folder contains the following files:
- The algorithms in one `.py` file
- The utility functions for the algorithms
- The table class
- requirements.txt

The app was created using streamlit module, and can be run using the following command:
```streamlit run app.py```. The deployed version of the app can be found [here](https://herminegrigoryan-ai-project-appapp-k6xyaq.streamlit.app/).

The **results** folder contains the subfolders of the csv files for each algorithm for different board sizes.

In order to do simulations and obtain the csv files as an output, you can run ```bash run_[algorithm_name].sh``` from the root directory by fixing the required parameters from the shell scripts.
