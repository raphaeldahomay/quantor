import math
from fredapi import Fred

fred = Fred(api_key="acb2d179d51fb6dde4b7a8e3a4839ce3")


def forward_future_prices(so, t, inc=0, q=0, storage=0, u=0, conv_y=0, r_foreign=0):
    base_t = round(float(t), 3)
    if base_t < 1:
        if base_t >= 0.5:
            if base_t == 0.5:
                final_rf = fred.get_series(f"DGS6MO").dropna().values[-1] / 100
            else:
                low_t = 0.5
                spread = base_t - low_t
                rf_low = fred.get_series(f"DGS6MO").dropna().values[-1]/ 100
                rf_up = fred.get_series(f"DGS1").dropna().values[-1] / 100
                final_rf = rf_low + spread * (rf_up - rf_low)
        elif base_t >= 0.25:
            if base_t == 0.25:
                final_rf = fred.get_series(f"DGS3MO").values[-1] / 100
            else:
                low_t = 0.25
                spread = base_t - low_t
                rf_low = fred.get_series(f"DGS3MO").dropna().values[-1] / 100
                rf_up = fred.get_series(f"DGS6MO").dropna().values[-1] / 100
                final_rf = rf_low + spread * (rf_up - rf_low)
        elif base_t >= round(1/12, 3):
            if base_t == round(1/12, 3):
                final_rf = fred.get_series(f"DGS1MO").dropna().values[-1] / 100
            else:
                low_t = 1/12
                spread = base_t - low_t
                rf_low = fred.get_series(f"DGS1MO").dropna().values[-1] / 100
                rf_up = fred.get_series(f"DGS3MO").dropna().values[-1] / 100
                final_rf = rf_low + spread * (rf_up - rf_low)
        else:
            final_rf = fred.get_series(f"DGS1MO").dropna().values[-1] / 100
    else:
        int_t = int(base_t)
        if base_t == int_t:
            final_rf = fred.get_series(f"DGS{int_t}").dropna().values[-1] / 100
        else:
            int_t_up = int_t + 1
            rf_low = fred.get_series(f"DGS{int_t}").dropna().values[-1] / 100
            rf_up = fred.get_series(f"DGS{int_t_up}").dropna().values[-1] / 100
            spread = base_t - int_t
            final_rf = rf_low + spread * (rf_up - rf_low)
    rf_adj = math.log(1 + final_rf)
    return round((so - inc + storage) * math.exp((rf_adj - q + u - conv_y - r_foreign) * t), 4)



def value_forward_futures(so, t, k, type="long"):
    base_t = round(float(t), 3)
    if base_t < 1:
        if base_t >= 0.5:
            if base_t == 0.5:
                final_rf = fred.get_series(f"DGS6MO").dropna().values[-1] / 100
            else:
                low_t = 0.5
                spread = base_t - low_t
                rf_low = fred.get_series(f"DGS6MO").dropna().values[-1]/ 100
                rf_up = fred.get_series(f"DGS1").dropna().values[-1] / 100
                final_rf = rf_low + spread * (rf_up - rf_low)
        elif base_t >= 0.25:
            if base_t == 0.25:
                final_rf = fred.get_series(f"DGS3MO").values[-1] / 100
            else:
                low_t = 0.25
                spread = base_t - low_t
                rf_low = fred.get_series(f"DGS3MO").dropna().values[-1] / 100
                rf_up = fred.get_series(f"DGS6MO").dropna().values[-1] / 100
                final_rf = rf_low + spread * (rf_up - rf_low)
        elif base_t >= round(1/12, 3):
            if base_t == round(1/12, 3):
                final_rf = fred.get_series(f"DGS1MO").dropna().values[-1] / 100
            else:
                low_t = 1/12
                spread = base_t - low_t
                rf_low = fred.get_series(f"DGS1MO").dropna().values[-1] / 100
                rf_up = fred.get_series(f"DGS3MO").dropna().values[-1] / 100
                final_rf = rf_low + spread * (rf_up - rf_low)
        else:
            final_rf = fred.get_series(f"DGS1MO").dropna().values[-1] / 100
    else:
        int_t = int(base_t)
        if base_t == int_t:
            final_rf = fred.get_series(f"DGS{int_t}").dropna().values[-1] / 100
        else:
            int_t_up = int_t + 1
            rf_low = fred.get_series(f"DGS{int_t}").dropna().values[-1] / 100
            rf_up = fred.get_series(f"DGS{int_t_up}").dropna().values[-1] / 100
            spread = base_t - int_t
            final_rf = rf_low + spread * (rf_up - rf_low)
    rf_adj = math.log(1 + final_rf)
    if type == "long":
        return so - k * math.exp(-rf_adj * t)
    else:
        return k * math.exp(-rf_adj * t) - so