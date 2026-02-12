import math

def var(array: list):
    n = len(array)
    mean_a = sum(array) / n
    var = sum((xi - mean_a)**2 for xi in array) / (n - 1)
    return round(var, 4) 


def std_or_downside_dev(x):
    return round(math.sqrt(x) * 100, 2)


def semi_var(array: list, tgt=None):
    n = len(array)
    mean_a = sum(array) / n
    if tgt:
        var = sum(min(0, (xi - tgt))**2 for xi in array) / (n - 1)
    var = sum(min(0, (xi - mean_a))**2 for xi in array) / (n - 1)
    return round(var, 4)