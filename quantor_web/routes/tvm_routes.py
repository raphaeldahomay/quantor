from flask import render_template, Blueprint, request, redirect, url_for
from engine.tvm.basic_tvm import pv_ordinary_due, fv_future_cfs, find_irr, pv_perpetuity, pv_growing_perpetuity, pv_all_kind, fv_all_kind

tvm = Blueprint('tvm_routes', __name__, url_prefix='/tvm')


@tvm.route('/formulas')
def tvm_formulas():
    return render_template('tvm/tvm.html')


@tvm.route("/simple_pv", methods=["POST"])
def calc_simple_pv():
    fv = float(request.form["fv"])
    r = float(request.form["r"])
    n = int(request.form["n"])
    type = request.form["type"]

    result_simple_pv = pv_all_kind(fv, r, n, type)

    return render_template('tvm/tvm.html', result_simple_pv=f"{result_simple_pv:,}")


@tvm.route("/simple_fv", methods=["POST"])
def calc_simple_fv():
    pv = float(request.form["pv"])
    r = float(request.form["r"])
    n = int(request.form["n"])
    type = request.form["type"]

    result_simple_fv = fv_all_kind(pv, r, n, type)

    return render_template('tvm/tvm.html', result_simple_fv=f"{result_simple_fv:,}")


@tvm.route("/stand_annuity", methods=["POST"])
def calc_stand_annuity():
    cf = float(request.form["cf"])
    r = float(request.form["r"])
    n = int(request.form["n"])
    when = request.form["when"]

    result_ann_stand = pv_ordinary_due(cf, r, n, when)

    return render_template('tvm/tvm.html', result_ann_stand=f"{result_ann_stand:,}")


@tvm.route("/fv_annuity", methods=["POST"])
def calc_fv_annuity():
    cf = float(request.form["cf"])
    r = float(request.form["r"])
    n = int(request.form["n"])
    when = request.form["when"]

    result_fv_ann = fv_future_cfs(cf, r, n, when)

    return render_template('tvm/tvm.html', result_fv_ann=f"{result_fv_ann:,}")


@tvm.route("/irr", methods=["POST"])
def calc_irr():
    iv = float(request.form["iv"])
    cf = float(request.form["cf"])
    n = int(request.form["n"])

    result_irr = find_irr(iv, cf, n)

    return render_template('tvm/tvm.html', result_irr=result_irr)


@tvm.route("/pv_perpetuity", methods=["POST"])
def calc_pv_perp():
    cf = float(request.form["cf"])
    r = float(request.form["r"])

    result_pv_perp = pv_perpetuity(cf, r)

    return render_template('tvm/tvm.html', result_pv_perp=result_pv_perp)


@tvm.route("/pv_grow_perpetuity", methods=["POST"])
def calc_pv_grow_perp():
    cf = float(request.form["cf"])
    r = float(request.form["r"])
    g = float(request.form["g"])

    result_pv_grow_perp = pv_growing_perpetuity(cf, r, g)

    return render_template('tvm/tvm.html', result_pv_grow_perp=result_pv_grow_perp)


@tvm.route("/formulas/form_details")
def see_tvm_form_details():
    return render_template('tvm/formula_details.html')