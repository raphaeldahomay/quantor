from flask import render_template, Blueprint, request, redirect, url_for
from engine.tvm.basic_tvm import pv_ordinary_due, fv_future_cfs, find_irr, pv_perpetuity, pv_growing_perpetuity, pv_all_kind, fv_all_kind

rnd = Blueprint('rnd_routes', __name__, url_prefix='/rnd')


@rnd.route('/prob_formulas')
def prob_formulas():
    return render_template('rnd/prob.html')


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