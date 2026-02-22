import math
import re

def variance(array):
    arranged_array = re.split(r"[,;\s]+", array.strip())
    new_array = [float(i) for i in arranged_array]
    n = len(new_array)
    mean_a = sum(new_array) / n
    var = sum((xi - mean_a)**2 for xi in new_array) / (n - 1)
    return round(var, 6) 


def std_or_downside_dev(x):
    return round(math.sqrt(x) * 100, 2)


def semi_var(array, tgt=None):
    arranged_array = re.split(r"[,;\s]+", array.strip())
    new_array = [float(i) for i in arranged_array]
    n = len(new_array)
    mean_a = sum(new_array) / n
    if tgt is not None:
        var = sum(min(0, (xi - tgt))**2 for xi in new_array) / (n - 1)
    var = sum(min(0, (xi - mean_a))**2 for xi in new_array) / (n - 1)
    return round(var, 6)