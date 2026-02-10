from scipy.stats import norm


def norm_cdf(z, mu=0, sig=1):
    return norm.cdf(z, loc=mu, scale=sig)


def inv_cdf(p, mu=0, sig=1):
    return norm.ppf(p, loc=mu, scale=sig)


def z_conversion(v, mu, sig):
    return round((v - mu) / sig, 2)