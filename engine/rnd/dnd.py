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
    # 1) robust row split: handles \n, \r\n, \r
    rows = str_returns.strip().splitlines()

    # 2) robust column split: handles tabs OR any amount of spaces (or mixes)
    table = [re.split(r"[;\t ]+", r.strip()) for r in rows if r.strip() != ""]

    # optional: clean out any accidental empty strings (safety)
    table = [[x for x in row if x != ""] for row in table]

    if v_format == "column":
        clean_table = np.array(table, dtype=float)       # n obs x n assets
    else:
        clean_table = np.array(table, dtype=float).T     # n obs x n assets

    # ---- your math (kept same style) ----
    mean_col = np.array([np.mean(clean_table[:, j]) for j in range(clean_table.shape[1])]).reshape(1, -1)  # 1 x n assets
    col_1 = np.ones(shape=(clean_table.shape[0], 1))  # n obs x 1

    first_p = (clean_table - (col_1 @ mean_col)).T
    second_p = clean_table - (col_1 @ mean_col)

    return np.round((1 / (clean_table.shape[0] - 1)) * (first_p @ second_p), 4)



def port_var_f_mat(str_returns, weights, v_format="column"):
    # Robust split: handles \n / \r\n (via splitlines), tabs, commas, semicolons, and spaces
    if "\n" in weights or "\r" in weights:
        row = weights.strip().splitlines()
    else:
        row = re.split(r"[,\t; ]+", weights.strip())

    # Clean empties (in case of multiple separators)
    row = [x for x in row if x != ""]

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



def div_effect(str_returns, weights, v_format="column"):
    cov_mat = cov_matrix(str_returns, v_format)
    size = cov_mat.shape[0]

    # std of each asset (from diagonal variances)
    std_list = [(std_or_downside_dev(cov_mat[i, i]) / 100) for i in range(size)]
    std_list_adj = np.array(std_list).reshape(1, -1)  # 1 x n_assets

    # Robust weights parsing (tabs, newlines, commas, semicolons, spaces, mixed)
    if "\n" in weights or "\r" in weights:
        row = weights.strip().splitlines()
    else:
        row = re.split(r"[,\t; ]+", weights.strip())
    row = [x for x in row if x != ""]

    clean_table = np.array(row, dtype=float).reshape(-1, 1)  # n_assets x 1

    # Safety check: weights length must match number of assets
    if clean_table.shape[0] != size:
        raise ValueError(f"weights length ({clean_table.shape[0]}) != number of assets ({size})")

    # Aggregate (weighted) average of individual std devs
    agg_std = (std_list_adj @ clean_table).item()  # scalar

    # Portfolio std dev
    port_std = std_or_downside_dev(port_var_f_mat(str_returns, weights, v_format)) / 100

    return round(agg_std - port_std, 6)