from engine.tvm.rates import discount_factor, capitalisation_factor, cap_factor_cont, disc_factor_cont


def pv_all_kind(fv: float, r: float, n: int, type="std_comp") -> float:
    if type == "linear":
        return round(fv / (1 + r * n), 2)
    elif type == "std_comp":
        return round(fv * discount_factor(r, n), 2)
    else:
        return round(fv * disc_factor_cont(r, n), 2)
    

def fv_all_kind(pv: float, r: float, n: int, type="std_cap") -> float:
    if type == "linear":
        return round(pv * (1 + r * n), 2)
    elif type == "std_cap":
        return round(pv * capitalisation_factor(r, n), 2)
    else:
        return round(pv * cap_factor_cont(r, n), 2)


def pv_future_cfs(cf: float, r: float, n: int, when: str = "end") -> float:
    if n < 0:
        raise ValueError("n must be >= 0")
    if when not in {"end", "begin"}:
        raise ValueError("when must be 'end' or 'begin'")

    sum_cf = 0.0

    if when == "end":
        # t = 1..n
        t = 1
        while t <= n:
            sum_cf += cf * discount_factor(r, t)
            t += 1
    else:
        # t = 0..n-1
        t = 0
        while t <= n - 1:
            sum_cf += cf * discount_factor(r, t)
            t += 1

    return sum_cf


def pv_ordinary_due(cf: float, r: float, n: int, when: str = "end") -> float:
    if r == 0:
        raise ValueError("r must be not be equal to 0")
    if when not in {"end", "begin"}:
        raise ValueError("when must be 'end' or 'begin'")
    
    if when == "end":
        pv = cf * (1 - (1 + r) ** (-n)) / r
    else:
        pv = (cf * (1 - (1 + r) ** (-n)) / r) * (1 + r)
    
    return round(pv, 2)


def fv_future_cfs(cf: float, r: float, n: int, when: str = "end") -> float:
    if n < 0:
        raise ValueError("n must be >= 0")
    if when not in {"end", "begin"}:
        raise ValueError("when must be 'end' or 'begin'")

    sum_cf = 0.0

    if when == "end":
        # payments at t=1..n, compound each to time n by (n - t)
        t = 1
        while t <= n:
            sum_cf += cf * capitalisation_factor(r, n - t)
            t += 1
    else:
        # payments at t=0..n-1, compound each to time n by (n - t)
        t = 0
        while t <= n - 1:
            sum_cf += cf * capitalisation_factor(r, n - t)
            t += 1

    return round(sum_cf, 2)


def pv_perpetuity(cf: float, r: float) -> float:
    if r == 0:
        return "r cannot be equal to 0"
    return round(cf / r, 2)


def pv_growing_perpetuity(cf: float, r: float, g: float) -> float:
    if r == g:
        return "r must not be equal to g"
    return round(cf / (r - g), 2)


def find_irr(iv: float, cf: float, n: int, tolerance: float = 1e-6) -> float:

    low, high = 0.0, 1.0
    
    if cf * n < iv:
        return "The product of your CF times the n must be higher than the I" 

    for _ in range(100):  # Limit iterations to prevent infinite loops
        r = (low + high) / 2
        
        if r == 0:
            npv = (cf * n) - iv
        else:
            pv = cf * (1 - (1 + r) ** (-n)) / r
            npv = pv - iv

        if abs(npv) < tolerance:
            return round(r * 100, 2)

        if npv > 0:
            low = r  # Rate is too low, increase it
        else:
            high = r # Rate is too high, decrease it
            
    return round(r * 100, 2)
