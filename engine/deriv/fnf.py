import math
from fredapi import Fred

fred = Fred(api_key="acb2d179d51fb6dde4b7a8e3a4839ce3")


def forward_future_prices(so, t, inc=0, q=0, storage=0, u=0, conv_y=0):  # think of removing the NaN inside the DF rtrived
    base_t = float(t)
    if base_t < 1:
        if base_t >= 0.5:
            low_t = 0.5
        sth = 0  # develop the logic
    else:
        int_t = int(base_t)
        if base_t == int_t:
            final_rf = fred.get_series(f"DGS{int_t}").values[-1]
        else:
            int_t_up = int_t + 1
            rf_low = fred.get_series(f"DGS{int_t}").values[-1]
            rf_up = fred.get_series(f"DGS{int_t_up}").values[-1]
            spread = base_t - int_t
            final_rf = rf_low + spread * (rf_up - rf_low)
    return (so - inc + storage) * math.exp((final_rf - q + u - conv_y) * t)