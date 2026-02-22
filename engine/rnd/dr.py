from engine.rnd.rm import variance
import math
import re


def skewness(array):
    var = variance(array)
    arranged_array = re.split(r"[,;\s]+", array.strip())
    new_array = [float(i) for i in arranged_array]
    n = len(new_array)
    mean_a = sum(new_array) / n
    skewn = (1 / (var * math.sqrt(var))) * sum((xi - mean_a)**3 for xi in new_array) / (n - 1)
    return round(skewn, 6)


def kurtosis(array):
    var = variance(array)
    arranged_array = re.split(r"[,;\s]+", array.strip())
    new_array = [float(i) for i in arranged_array]
    n = len(new_array)
    mean_a = sum(new_array) / n
    kurt = ((1 / (var ** 2)) * sum((xi - mean_a)**4 for xi in new_array) / (n - 1)) - 3
    return round(kurt, 6)