from engine.rnd.dnd import port_var_f_mat
from engine.rnd.prob import inv_cdf
from engine.rnd.rm import std_or_downside_dev
import numpy as np


def var_f_mat(returns, weights, conf):
    p_var = port_var_f_mat(returns, weights)
    row = returns.strip().split("\n")
    table = [r.split("\t") for r in row]
    clean_table = np.array(table, dtype=float) # n observations x n assets
    assets = np.array([clean_table[:, j] for j in range(clean_table.shape[1])]) # n assets x n observations
    mean_col = np.array([np.mean(assets[j, :]) for j in range(assets.shape[0])]).reshape(1, -1)
    if "\n" in weights:
        row = weights.strip().split("\n")
    else:
        row = weights.strip().split("\t")
    clean_table_w = np.array(row, dtype=float).reshape(-1, 1)
    mu = mean_col @ clean_table_w
    std = std_or_downside_dev(p_var) / 100
    phi = inv_cdf(conf, mu, std)
    return (std * phi) - mu


# Add formula of standard VaR, CVaR, Historical VaR, 
# Add formula of matrix ES, standard ES, Historical ES