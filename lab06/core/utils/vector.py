from functools import reduce
import numpy as np

def norm2(v) -> float:
    return reduce(lambda acc, x: acc + x**2, v, 0)**.5

def sparse_to_dense(v, n, horizontal = True) -> np.ndarray:
    d = np.zeros(n)
    key = "row" if horizontal else "col"
    for el in v:
        d[el[key]] = el["value"]
    
    return d
