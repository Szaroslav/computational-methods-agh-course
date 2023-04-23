import os
import numpy as np
import json_stream

if __name__ == "__main__":
    import constants
else:
    import db.constants as constants

dt = np.dtype([("row", np.uint32), ("col", np.uint32), ("value", np.float32)])

sparse_matrix_dims = None
sparse_matrix = None
scipy_s_matrix = None
bow = None
U, D, V = None, None, None
S = None


def get_contents(indicies):
    indicies_dict = { idx: new_idx for new_idx, idx in enumerate(indicies) }
    indicies = np.sort(indicies)
    contents = [None for _ in range(len(indicies))]

    with open(f"{os.path.dirname(__file__)}/{constants.FILES_PATH}/{constants.DOCUMENTS_NAME}", "r", encoding="utf8") as file:
        data = json_stream.load(file)

        j = 0
        for i, d in enumerate(data):
            if i == indicies[j]:
                contents[indicies_dict[i]] = d
                j += 1
                if j >= len(indicies): break

    return contents
