from functools import reduce

def norm2(v) -> float:
    return reduce(lambda acc, x: acc + x**2, v, 0)**.5