from flask import render_template, Blueprint, request, redirect, url_for
from engine.rnd.prob import z_conversion, norm_cdf, inv_cdf, es_coeff
from engine.rnd.rm import variance, std_or_downside_dev, semi_var

rnd = Blueprint('rnd_routes', __name__, url_prefix='/rnd')


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



@rnd.route('/dnr_formulas')
def dnr_formulas():
    return render_template('rnd/dnr.html')


@rnd.route('/dnd_formulas')
def dnd_formulas():
    return render_template('rnd/dnd.html')


@rnd.route('/tail_formulas')
def tail_formulas():
    return render_template('rnd/tail.html')


@rnd.route('/radj_formulas')
def radj_formulas():
    return render_template('rnd/radj.html')


@rnd.route('/scen_formulas')
def scen_formulas():
    return render_template('rnd/scen.html')