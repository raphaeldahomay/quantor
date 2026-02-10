from flask import render_template, Blueprint, request, redirect, url_for
from engine.rnd.prob import z_conversion, norm_cdf, inv_cdf

rnd = Blueprint('rnd_routes', __name__, url_prefix='/rnd')


@rnd.route('/prob_formulas')
def prob_formulas():
    return render_template('rnd/prob.html')


@rnd.route('/prob_formulas',  methods=["POST"])
def calc_z_score():
    v = float(request.form["v"])
    mu = float(request.form["mu"])
    sig = float(request.form["sig"])

    z_socre = z_conversion(v, mu, sig)

    return render_template('rnd/prob.html', z_socre=f"{z_socre:,}")


@rnd.route("/prob_formulas/form_details_1")
def see_rnd_form_1():
    return render_template('rnd/formula_details/form_1.html')


@rnd.route('/rm_formulas')
def rm_formulas():
    return render_template('rnd/rm.html')


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