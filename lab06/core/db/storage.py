import numpy as np

dt = np.dtype([("row", np.uint32), ("col", np.uint32), ("value", np.float32)])

sparse_matrix_dims = None
sparse_matrix = None
scipy_s_matrix = None
bow = None
U, D, V = None, None, None
S = None