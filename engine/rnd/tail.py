from engine.rnd.dnd import port_var_f_mat
from engine.rnd.prob import inv_cdf, es_coeff
from engine.rnd.rm import std_or_downside_dev
from engine.rnd.dr import skewness_multiple, kurtosis_multiple
import numpy as np
import re


def var_es_f_mat(returns, weights, conf=0.95, type="var", v_format="column"):
    p_var = port_var_f_mat(returns, weights, v_format)
    row = returns.strip().split("\n")
    table = [r.split("\t") for r in row]
    clean_table = np.array(table, dtype=float) # n observations x n assets
    assets = np.array([clean_table[:, j] for j in range(clean_table.shape[1])]) # n assets x n observations
    mean_col = np.array([np.mean(assets[j, :]) for j in range(assets.shape[0])]).reshape(1, -1)
    row = re.split(r"[,\s;]+", weights.strip())
    clean_table_w = np.array(row, dtype=float).reshape(-1, 1)
    mu = (mean_col @ clean_table_w)[0, 0]
    std = std_or_downside_dev(p_var) / 100
    if type == "var":
        phi = inv_cdf(conf, mu, std)
    elif type == "es":
        phi = es_coeff(conf, mu, std)
    else:
        return "please enter a valid option"
    return round((std * phi) - mu, 6)


def hist_var_es(
    returns_raw: str,
    positions,
    assets_axis: str = "cols",   # "cols" => assets are columns (n_obs x n_assets)
    risk: str = "var",           # "var" or "es"
    conf: float = 0.95
) -> float:

    # --------- small helpers ----------
    def _parse_positions(pos):
        if isinstance(pos, (list, tuple, np.ndarray)):
            arr = np.asarray(pos, dtype=float).reshape(-1)
            return arr

        if isinstance(pos, str):
            parts = re.split(r"[,\s;]+", pos.strip())
            parts = [p for p in parts if p != ""]
            return np.asarray(parts, dtype=float).reshape(-1)

        raise TypeError("positions must be array-like or a string.")

    def _parse_returns_table(s: str):
        # split into rows by newline
        lines = [ln.strip() for ln in s.strip().splitlines() if ln.strip() != ""]
        if not lines:
            raise ValueError("returns_raw is empty.")

        table = []
        for ln in lines:
            parts = re.split(r"[,\t\s;]+", ln.strip())
            parts = [p for p in parts if p != ""]
            table.append([float(x) for x in parts])

        ncols = len(table[0])
        if any(len(r) != ncols for r in table):
            raise ValueError("returns_raw has inconsistent row lengths (not a clean table).")

        return np.asarray(table, dtype=float)

    # --------- validation ----------
    if not (0 < conf < 1):
        raise ValueError("conf must be in (0,1), e.g. 0.95.")

    risk = risk.strip().lower()
    if risk not in {"var", "es"}:
        raise ValueError("risk must be 'var' or 'es'.")

    assets_axis = assets_axis.strip().lower()
    if assets_axis not in {"cols", "rows"}:
        raise ValueError("assets_axis must be 'cols' or 'rows'.")

    R = _parse_returns_table(returns_raw)
    w = _parse_positions(positions)

    # orient table to (n_obs x n_assets)
    if assets_axis == "rows":
        R = R.T

    n_obs, n_assets = R.shape
    if w.shape[0] != n_assets:
        raise ValueError(f"positions length ({w.shape[0]}) must match n_assets ({n_assets}).")

    if n_obs < 2:
        raise ValueError("Need at least 2 observations.")

    # --------- portfolio P&L / losses ----------
    port_ret = R @ w  # shape: (n_obs,)
    losses = -port_ret  # positive = loss

    # --------- Historical VaR / ES ----------
    alpha = conf
    var = float(np.quantile(losses, alpha))

    if risk == "var":
        return round(var, 6)

    tail = losses[losses >= var]
    if tail.size == 0:
        return var
    es = float(tail.mean())
    return round(es, 6)



import math

def cornish_fisher_var(str_returns, weights, conf=0.95, v_format="column"):

    fmt = v_format.lower()
    orientation = "column" if fmt.startswith("col") else "row"

    # portfolio sigma
    sigma = math.sqrt(port_var_f_mat(str_returns, weights, v_format=orientation))

    # portfolio skewness and excess kurtosis (already aggregated using weights)
    gamma1 = skewness_multiple(str_returns, weights, orientation=orientation)
    eK = kurtosis_multiple(str_returns, weights, orientation=orientation)

    # standard normal quantile
    z = inv_cdf(conf, mu=0, sig=1)

    # Cornish–Fisher adjusted quantile
    z_cf = (
        z
        + (1/6)  * (z**2 - 1)       * gamma1
        + (1/24) * (z**3 - 3*z)     * eK
        - (1/36) * (2*z**3 - 5*z)   * (gamma1**2)
    )

    # VaR as a positive loss magnitude
    var_cf = (z_cf * sigma)
    return round(var_cf, 6)