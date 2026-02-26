from flask import render_template, Blueprint, request, redirect, url_for
import numpy as np
from engine.rnd.prob import z_conversion, norm_cdf, inv_cdf, es_coeff
from engine.rnd.rm import variance, std_or_downside_dev, semi_var
from engine.rnd.dnd import corr, cov, cov_matrix, port_var_f_mat, port_var_hand_2_assets, div_effect
from engine.rnd.dr import skewness_multiple, skewness_single, kurtosis_multiple, kurtosis_single
from engine.rnd.tail import var_es_f_mat, hist_var_es, cornish_fisher_var

rnd = Blueprint('rnd_routes', __name__, url_prefix='/rnd')


# < ---- All routes related to Uncertainty Modeling ---- >

@rnd.route('/prob_formulas')
def prob_formulas():
    return render_template('rnd/prob.html')


@rnd.route('/prob_formulas/zscore',  methods=["POST"])
def calc_z_score():
    v = float(request.form["v"])
    mu = float(request.form["mu"])
    sig = float(request.form["sig"])
    z_score = z_conversion(v, mu, sig)
    return render_template('rnd/prob.html', z_score=f"{z_score:,}")


@rnd.route('/prob_formulas/es_coeff',  methods=["POST"])
def calc_es_coeff():
    p = float(request.form["p"])
    mu = float(request.form["mu"])
    sig = float(request.form["sig"])
    es_c = es_coeff(p, mu, sig)
    return render_template('rnd/prob.html', es_c=f"{es_c:,}")


@rnd.route('/prob_formulas/std_cdf',  methods=["POST"])
def calc_std_norm_cdf():
    z = float(request.form["z"])
    p_std = norm_cdf(z)
    return render_template('rnd/prob.html', p_std=f"{p_std:,}")


@rnd.route('/prob_formulas/norm_cdf',  methods=["POST"])
def calc_norm_cdf():
    z = float(request.form["z"])
    mu = float(request.form["mu"])
    sig = float(request.form["sig"])
    p = norm_cdf(z, mu, sig)
    return render_template('rnd/prob.html', p=f"{p:,}")


@rnd.route('/prob_formulas/std_inv',  methods=["POST"])
def calc_std_inv_cdf():
    p = float(request.form["p"])
    z_std = inv_cdf(p)
    return render_template('rnd/prob.html', z_std=f"{z_std:,}")


@rnd.route('/prob_formulas/norm_inv',  methods=["POST"])
def calc_inv_cdf():
    p = float(request.form["p"])
    mu = float(request.form["mu"])
    sig = float(request.form["sig"])
    z = inv_cdf(p, mu, sig)
    return render_template('rnd/prob.html', z=f"{z:,}")


@rnd.route("/prob_formulas/form_details_1")
def see_rnd_form_1():
    return render_template('rnd/formula_details/form_1.html')


@rnd.route("/prob_formulas/form_details_2")
def see_rnd_form_2():
    return render_template('rnd/formula_details/form_2.html')


@rnd.route("/prob_formulas/form_details_3")
def see_rnd_form_3():
    return render_template('rnd/formula_details/form_3.html')


@rnd.route("/prob_formulas/form_details_4")
def see_rnd_form_4():
    return render_template('rnd/formula_details/form_4.html')




# < ---- All routes related to Risk Measurement ---- >

@rnd.route('/rm_formulas')
def rm_formulas():
    return render_template('rnd/rm.html')


@rnd.route('/rm_formulas/variance', methods=["POST"])
def calc_variance():
    ar = request.form["r"]
    final_variance = variance(ar)
    return render_template('rnd/rm.html', final_variance=final_variance)


@rnd.route('/rm_formulas/std_dev', methods=["POST"])
def calc_std_dev():
    v = float(request.form["v"])
    final_std = std_or_downside_dev(v)
    return render_template('rnd/rm.html', final_std=final_std)


@rnd.route('/rm_formulas/semi_var', methods=["POST"])
def calc_semi_var():
    ar = request.form["r"]
    if request.form["t"] == "":
        final_semi_var = semi_var(ar)
        return render_template('rnd/rm.html', final_semi_var=final_semi_var)
    t = float(request.form["t"])
    final_semi_var = semi_var(ar, tgt=t)
    return render_template('rnd/rm.html', final_semi_var=final_semi_var)


@rnd.route("/prob_formulas/form_details_5")
def see_rnd_form_5():
    return render_template('rnd/formula_details/form_5.html')




# < ---- All routes related to Dependence Risk & Diversification ---- >

@rnd.route('/dnd_formulas')
def dnd_formulas():
    result_cov_mat = None
    return render_template('rnd/dnd.html', result_cov_mat=result_cov_mat)


@rnd.route('/dnd_formulas/covariance', methods=["POST"])
def calc_covariance():
    ar_1 = request.form["ar_1"]
    ar_2 = request.form["ar_2"]
    result_cov = cov(ar_1, ar_2)
    return render_template('rnd/dnd.html', result_cov=result_cov)


@rnd.route('/dnd_formulas/corr', methods=["POST"])
def calc_corr():
    ar_1 = request.form["ar_1"]
    ar_2 = request.form["ar_2"]
    result_corr = corr(ar_1, ar_2)
    return render_template('rnd/dnd.html', result_corr=result_corr)


@rnd.route('/dnd_formulas/cov_mat', methods=["POST"])
def calc_cov_mat():
    array_s = request.form["array_s"]
    forma = request.form["forma"]
    result_cov_mat = np.array2string(cov_matrix(array_s, forma), precision=6, suppress_small=True)
    return render_template('rnd/dnd.html', result_cov_mat=result_cov_mat)


@rnd.route('/dnd_formulas/port_var_mat', methods=["POST"])
def calc_port_var_mat():
    array_s = request.form["array_s"]
    weigh = request.form["weigh"]
    forma = request.form["forma"]
    result_port_var_mat = port_var_f_mat(array_s, weigh, forma)
    return render_template('rnd/dnd.html', result_port_var_mat=result_port_var_mat)


@rnd.route('/dnd_formulas/port_var_2_assets', methods=["POST"])
def calc_port_var_2_assets():
    ar_1 = request.form["ar_1"]
    ar_2 = request.form["ar_2"]
    weigh = request.form["weigh"]
    result_port_var_2_assets = port_var_hand_2_assets(ar_1, ar_2, weigh)
    return render_template('rnd/dnd.html', result_port_var_2_assets=result_port_var_2_assets)


@rnd.route('/dnd_formulas/div_effect', methods=["POST"])
def calc_div_effect():
    array_s = request.form["array_s"]
    weigh = request.form["weigh"]
    forma = request.form["forma"]
    result_div_effect = div_effect(array_s, weigh, forma)
    return render_template('rnd/dnd.html', result_div_effect=result_div_effect)


@rnd.route("/prob_formulas/form_details_dnd")
def see_rnd_form_dnd():
    return render_template('rnd/formula_details/form_dnd.html')




# < ---- All routes related to Distribution Risk ---- >

@rnd.route('/dr_formulas')
def dr_formulas():
    return render_template('rnd/dr.html')


@rnd.route('/dr_formulas/skewness_single', methods=["POST"])
def calc_skewness_sing():
    ar_1 = request.form["ar_1"]
    result_skew_s = skewness_single(ar_1)
    return render_template('rnd/dr.html', result_skew_s=result_skew_s)


@rnd.route('/dr_formulas/skewness_multiple', methods=["POST"])
def calc_skewness_multip():
    ar_1 = request.form["ar_1"]
    weigh = request.form["weigh"]
    forma = request.form["forma"]
    result_skew_m = skewness_multiple(ar_1, weigh, forma)
    return render_template('rnd/dr.html', result_skew_m=result_skew_m)


@rnd.route('/dr_formulas/kurtosis_single', methods=["POST"])
def calc_kurtosis_sing():
    ar_1 = request.form["ar_1"]
    result_kurt_s = kurtosis_single(ar_1)
    return render_template('rnd/dr.html', result_kurt_s=result_kurt_s)


@rnd.route('/dr_formulas/kurtosis_multiple', methods=["POST"])
def calc_kurtosis_multip():
    ar_1 = request.form["ar_1"]
    weigh = request.form["weigh"]
    forma = request.form["forma"]
    result_kurt_m = kurtosis_multiple(ar_1, weigh, forma)
    return render_template('rnd/dr.html', result_kurt_m=result_kurt_m)


@rnd.route("/prob_formulas/form_details_dr")
def see_rnd_form_dr():
    return render_template('rnd/formula_details/form_dr.html')





# < ---- All routes related to Tail Risk ---- >

@rnd.route('/tail_formulas')
def tail_formulas():
    return render_template('rnd/tail.html')


@rnd.route('/tail_formulas/var_es_standard', methods=["POST"])
def calc_stand_var_es():
    ar_1 = request.form["ar_1"]
    weigh = request.form["weigh"]
    typee = request.form["type"]
    forma = request.form["forma"]
    try:
        conf = request.form["conf"]
        result_var_es_stand = var_es_f_mat(ar_1, weigh, conf, typee, forma)
        return render_template('rnd/tail.html', result_var_es_stand=result_var_es_stand)
    except:
        pass
    result_var_es_stand = var_es_f_mat(ar_1, weigh, type=typee, v_format=forma)
    return render_template('rnd/tail.html', result_var_es_stand=result_var_es_stand)


@rnd.route('/tail_formulas/var_es_hist', methods=["POST"])
def calc_hist_var_es():
    ar_1 = request.form["ar_1"]
    weigh = request.form["weigh"]
    typee = request.form["type"]
    forma = request.form["forma"]
    try:
        conf = request.form["conf"]
        result_var_es_hist = hist_var_es(ar_1, weigh, forma, typee, conf)
        return render_template('rnd/tail.html', result_var_es_hist=result_var_es_hist)
    except:
        pass
    result_var_es_hist = hist_var_es(ar_1, weigh, forma, typee)
    return render_template('rnd/tail.html', result_var_es_hist=result_var_es_hist)


@rnd.route('/tail_formulas/cornish_var', methods=["POST"])
def calc_cornish_var():
    ar_1 = request.form["ar_1"]
    weigh = request.form["weigh"]
    forma = request.form["forma"]
    try:
        conf = request.form["conf"]
        result_cornish_var = cornish_fisher_var(ar_1, weigh, conf, forma)
        return render_template('rnd/tail.html', result_cornish_var=result_cornish_var)
    except:
        pass
    result_cornish_var = cornish_fisher_var(ar_1, weigh, v_format=forma)
    return render_template('rnd/tail.html', result_cornish_var=result_cornish_var)


@rnd.route("/prob_formulas/form_details_tail")
def see_rnd_form_tail():
    return render_template('rnd/formula_details/form_tail.html')