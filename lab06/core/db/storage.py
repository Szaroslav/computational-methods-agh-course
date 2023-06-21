import os
import numpy as np
import json_stream
from django.core.cache import cache

if __name__ == "__main__":
    import constants
else:
    import db.constants as constants

dt = np.dtype([("row", np.uint32), ("col", np.uint32), ("value", np.float32)])

sparse_matrix_dims: tuple[int, int] | None = None
sparse_matrix: np.ndarray | None = None
scipy_s_matrix = None
bow: dict[str, int] | None = None
U, D, V = None, None, None
S = None


def load():
    global sparse_matrix_dims, sparse_matrix, bow, S, U

    if not sparse_matrix_dims and cache.get("sparse_matrix_dims"):
        sparse_matrix_dims = cache.get("sparse_matrix_dims")
    elif not cache.get("sparse_matrix_dims"):
        raise ValueError("Sparse matrix dims are not set")

    if not bow and cache.get("bag_of_words"):
        bow = cache.get("bag_of_words")
    elif not cache.get("bag_of_words"):
        raise ValueError("Bag of words are not set")

    if cache.get("sparse_matrix") is not None:
        if sparse_matrix is None:
            sparse_matrix = cache.get("sparse_matrix")

    elif cache.get("S") is not None:
        if S is None:
            sparse_matrix = cache.get("S")

        if U is None and cache.get("U") is not None:
            U = cache.get("U")
        elif cache.get("U") is None:
            raise ValueError("U matrix is not set")

    else:
        raise ValueError("Cache is not set")


def get_contents(indicies):
    indicies_dict = {idx: new_idx for new_idx, idx in enumerate(indicies)}
    indicies = np.sort(indicies)
    contents = [None for _ in range(len(indicies))]

    with open(f"{os.path.dirname(__file__)}/{constants.FILES_PATH}/{constants.DOCUMENTS_NAME}", "r", encoding="utf8") as file:
        data = json_stream.load(file)

        j = 0
        for i, d in enumerate(data):
            if i == indicies[j]:
                contents[indicies_dict[i]] = d
                j += 1
                if j >= len(indicies):
                    break

    return contents
