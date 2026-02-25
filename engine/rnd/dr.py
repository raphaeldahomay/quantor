from engine.rnd.rm import variance
from engine.rnd.dnd import port_var_f_mat
import math
import re


def skewness_single(array):
    var = variance(array)

    arranged_array = re.split(r"[,;\s]+", array.strip())
    new_array = [float(i) for i in arranged_array]

    n = len(new_array)
    mean_a = sum(new_array) / n

    skewn = (1 / (var * math.sqrt(var))) * \
            (sum((xi - mean_a) ** 3 for xi in new_array) / (n - 1))

    return round(skewn, 6)



def kurtosis_single(array):
    var = variance(array)

    arranged_array = re.split(r"[,;\s]+", array.strip())
    new_array = [float(i) for i in arranged_array]

    n = len(new_array)
    mean_a = sum(new_array) / n

    kurt = ((1 / (var ** 2)) *
            (sum((xi - mean_a) ** 4 for xi in new_array) / (n - 1))) - 3

    return round(kurt, 6)



def skewness_multiple(matrix_str, weights, orientation="row"):

    # ---- Parse matrix ----
    rows = [r.strip() for r in matrix_str.strip().split("\n") if r.strip()]
    matrix = [list(map(float, re.split(r"[,\s;]+", r))) for r in rows]

    # ---- Parse weights ----
    w = list(map(float, re.split(r"[,\s;]+", weights.strip())))

    # ---- Adjust orientation ----
    if orientation == "column":
        matrix = list(zip(*matrix))  # transpose

    # ---- Check dimension ----
    if len(matrix) != len(w):
        raise ValueError("Number of weights must equal number of assets.")

    # ---- Build portfolio returns ----
    port_returns = []

    for t in range(len(matrix[0])):  # time dimension
        rp = sum(w[i] * matrix[i][t] for i in range(len(w)))
        print(rp)
        port_returns.append(rp)

    # ---- Convert to string to reuse single function ----
    port_str = " ".join(str(x) for x in port_returns)

    return skewness_single(port_str)



def kurtosis_multiple(matrix_str, weights, orientation="row"):

    rows = [r.strip() for r in matrix_str.strip().split("\n") if r.strip()]
    matrix = [list(map(float, re.split(r"[,\s;]+", r))) for r in rows]

    w = list(map(float, re.split(r"[,\s;]+", weights.strip())))

    if orientation == "column":
        matrix = list(zip(*matrix))

    if len(matrix) != len(w):
        raise ValueError("Number of weights must equal number of assets.")

    port_returns = []

    for t in range(len(matrix[0])):
        rp = sum(w[i] * matrix[i][t] for i in range(len(w)))
        port_returns.append(rp)

    port_str = " ".join(str(x) for x in port_returns)

    return kurtosis_single(port_str)