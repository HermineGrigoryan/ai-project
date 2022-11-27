import numpy as np
import copy

class Table():
    def __init__(self, row_shape, col_shape) -> None:
        self.row_shape = row_shape
        self.col_shape = col_shape

    def create_table(self):
        board = np.random.normal(loc = 0, scale = 1, size = (self.row_shape, self.col_shape))
        self.board = board
        return board

    def set_board(self, board):
        self.board = copy.deepcopy(board)
        return board

    @property
    def line_sums(self):
        row = self.board.sum(axis=1)
        col = self.board.sum(axis=0)
        return row, col 

    def get_row_changed(self, row_number):
        cur_board = copy.deepcopy(self.board)
        cur_board[row_number, :] = cur_board[row_number, :]*(-1)
        return cur_board

    def get_col_changed(self, col_number):
        cur_board = copy.deepcopy(self.board)
        cur_board[:, col_number] = cur_board[:, col_number]*(-1)
        return cur_board

    def randomize_board_signs(self, p):

        selected_row = np.random.choice(range(int(self.row_shape)), int(self.row_shape*p), replace=False)
        selected_col = np.random.choice(range(int(self.col_shape)), int(self.col_shape*p), replace=False)
        # print('selected_row:',selected_row)
        # print('selected_col',selected_col)
        randomized_board = self.board
        randomized_board[selected_row, :] = -1 * self.board[selected_row, :]
        randomized_board[:, selected_col] = -1 * self.board[:, selected_col]

        return randomized_board

    @property
    def if_goal(self):
        if np.min(np.append(self.line_sums[0],self.line_sums[1], axis=0))<0:
            return False
        return True