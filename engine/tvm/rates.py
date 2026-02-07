import math

def capitalisation_factor(r: float, n: int) -> float:
    """
    Capitalisation factor: moves value forward in time
    CF = (1 + r)^n
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    return (1 + r) ** n


def discount_factor(r: float, n: int) -> float:
    """
    Discount factor: moves value backward in time
    DF = 1 / (1 + r)^n
    """
    return 1 / capitalisation_factor(r, n)


def ear(apr: float, m: int) -> float:
    return ((1 + (apr / m)) ** m) - 1


def apr(ear: float, m: int) -> float:
    return ((1 + ear) ** (1 / m) - 1) * m


def cont_comp_rate(apr: float, m: int) -> float:
    return m * math.log(1 + apr)


def cap_factor_cont(r: float, n: int) -> float:
    return math.exp(r * n)


def disc_factor_cont(r: float, n: int) -> float:
    return 1 / cap_factor_cont(r, n)
