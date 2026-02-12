from engine.rnd.rm import var, std_or_downside_dev
import numpy as np

def cov(list_1: list, list_2: list):
    if len(list_1) != len(list_2):
        return "your inputs must be of the same length"
    n = len(list_1)
    mean_x = sum(list_1) / n
    mean_y = sum(list_2) / n
    cov = sum((xi - mean_x)*(yi - mean_y) for xi, yi in zip(list_1, list_2)) / (n - 1)
    return round(cov, 4)


def corr(list_1, list_2):
    if len(list_1) != len(list_2):
        return "your inputs must be of the same length"
    cova = cov(list_1, list_2)
    std_1 = std_or_downside_dev(var(list_1)) / 100
    std_2 = std_or_downside_dev(var(list_2)) / 100
    return round(cova / (std_1 * std_2), 2)


def cov_matrix(str_returns):
    rows = str_returns.strip().split("\n")
    table = [r.split("\t") for r in rows]
    clean_table = np.array(table, dtype=float) # n observations x n assets
    assets = np.array([clean_table[:, j] for j in range(clean_table.shape[1])]) # n assets x n observations
    mean_col = np.array([np.mean(assets[j, :]) for j in range(assets.shape[0])]) # (n_assets,)
    col_1 = np.ones((mean_col.shape[0], 1)) # n assets x 1
    mean_col = mean_col.reshape(1, -1) # (1, n_assets)
    first_p = (assets - (col_1 @ mean_col)) . T
    second_p = assets - (col_1 @ mean_col)
    return np.round((1 / (assets.shape[1] - 1)) * (first_p @ second_p), 4)


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

