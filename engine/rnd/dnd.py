from engine.rnd.rm import variance, std_or_downside_dev
import numpy as np

def cov(array_1, array_2):
    big_array = [array_1, array_2]
    new_array = []
    for a in big_array:
        if " " and "," in a:
            array_adj = a.strip().split(",")
            new_array.append([float(i) for i in array_adj])
        elif " " in a:
            array_adj = a.strip().split()
            new_array.append([float(i) for i in array_adj])
        elif "," in a:
            array_adj = a.strip().split(",")
            new_array.append([float(i) for i in array_adj])
        elif "\t" in a:
            array_adj = a.strip().split("\t")
            new_array.append([float(i) for i in array_adj])
        elif "\n" in a:
            array_adj = a.strip().split("\t")
            new_array.append([float(i) for i in array_adj])
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
    if v_format == "column":
        rows = str_returns.strip().split("\n")
        table = [r.split("\t") for r in rows]
        clean_table = np.array(table, dtype=float) # n obs x n assets
    mean_col = np.array([np.mean(clean_table[:, j]) for j in range(clean_table.shape[1])]).reshape(1, -1) # 1 x n assets
    col_1 = np.ones(shape=(clean_table.shape[0], 1)) # n obs x 1
    first_p = (clean_table - (col_1 @ mean_col)) . T
    second_p = clean_table - (col_1 @ mean_col)
    return np.round((1 / (clean_table.shape[0] - 1)) * (first_p @ second_p), 4)


def port_var_f_mat(str_returns, weights):
    if "\n" in weights:
        row = weights.strip().split("\n")
    else:
        row = weights.strip().split("\t")
    clean_table = np.array(row, dtype=float).reshape(1, -1)
    cov_mat = cov_matrix(str_returns)
    final_var = (clean_table @ cov_mat) @ (clean_table.T)
    return np.round(final_var[0, 0], 8)


def port_var_hand(big_list, w_list):
    result = sum(sum(wi * wj * cov(big_listi, big_listj) for wi, big_listi in zip(w_list, big_list)) for wj, big_listj in zip(w_list, big_list))
    return round(result, 8)

