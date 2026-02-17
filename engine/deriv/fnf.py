import math
from fredapi import Fred

fred = Fred(api_key="acb2d179d51fb6dde4b7a8e3a4839ce3")


def forward_future_prices(so, t, inc=0, q=0, storage=0, u=0, conv_y=0):
    round_t = round(float(t), 0)
    if float(t) != round_t:
        low_t = round(float(t))
        high_t = round(float(t) + 1)  # continue to code the logic around getting the low and t=high integer of any number
    rf = fred.get_series("DGS1").values[-1]
    return (so - inc + storage) * math.exp((rf - q + u - conv_y) * t)