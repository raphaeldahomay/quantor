from engine.rnd.rm import variance, std_or_downside_dev
import numpy as np
import re

def cov(array_1, array_2):
    big_array = [array_1, array_2]
    new_array = []
    for a in big_array:
        new_a = re.split(r"[,\s;]+", a.strip())
        n = [float(i) for i in new_a]
        new_array.append(n)
    if len(new_array[0]) != len(new_array[1]):
        return "your inputs must be of the same length"
    n = len(new_array[0])
    mean_x = sum(new_array[0]) / n
    mean_y = sum(new_array[1]) / n
    cov = sum((xi - mean_x)*(yi - mean_y) for xi, yi in zip(new_array[0], new_array[1])) / (n - 1)
    return round(cov, 4)


def corr(array_1, array_2):
    cova = cov(array_1, array_2)
    if type(cova) == str:
        return "your inputs must be of the same length"
    std_1 = std_or_downside_dev(variance(array_1)) / 100
    std_2 = std_or_downside_dev(variance(array_2)) / 100
    return round(cova / (std_1 * std_2), 2)


def cov_matrix(str_returns, v_format="column"):
    rows = str_returns.strip().split("\n")
    table = [r.split("\t") for r in rows]
    if v_format == "column":
        clean_table = np.array(table, dtype=float) # n obs x n assets
    else:
        clean_table = np.array(table, dtype=float) . T # n obs x n assets
    mean_col = np.array([np.mean(clean_table[:, j]) for j in range(clean_table.shape[1])]).reshape(1, -1) # 1 x n assets
    col_1 = np.ones(shape=(clean_table.shape[0], 1)) # n obs x 1
    first_p = (clean_table - (col_1 @ mean_col)) . T
    second_p = clean_table - (col_1 @ mean_col)
    return np.round((1 / (clean_table.shape[0] - 1)) * (first_p @ second_p), 4)


def port_var_f_mat(str_returns, weights, v_format="column"):
    if "\n" in weights:
        row = weights.strip().split("\n")
    elif "\t" in weights:
        row = weights.strip().split("\t")
    else:
        row_adj = weights.strip().split(",")
        row = [i.strip() for i in row_adj]
    clean_table = np.array(row, dtype=float).reshape(1, -1)
    cov_mat = cov_matrix(str_returns, v_format)
    final_var = (clean_table @ cov_mat) @ (clean_table.T)
    return np.round(final_var[0, 0], 8)


def port_var_hand_2_assets(list_r_1, list_r_2, w_list):
    big_list = [list_r_1, list_r_2]

    # split weights on comma OR any whitespace (space/tab/newline)
    parts = re.split(r"[,\s]+", w_list.strip())
    new_array = [float(x) for x in parts if x != ""]

    if len(new_array) != 2:
        return (f"You must provide exactly 2 weights. Got: {new_array}")

    result = sum(
        wi * wj * cov(big_listi, big_listj)
        for wi, big_listi in zip(new_array, big_list)
        for wj, big_listj in zip(new_array, big_list)
    )
    return round(result, 8)


# Add the formula for diversification effect