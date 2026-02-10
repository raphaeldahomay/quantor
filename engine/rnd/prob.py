from scipy.stats import norm


def norm_cdf(z, mu=0, sig=1):
    return round(norm.cdf(z, loc=mu, scale=sig) * 100, 2)


def inv_cdf(p, mu=0, sig=1):
    return round(norm.ppf(p, loc=mu, scale=sig), 2)


def z_conversion(v, mu, sig):
    return round((v - mu) / sig, 2)