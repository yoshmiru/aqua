from datetime import datetime
from io import BytesIO
# flask
from wtforms import Form, DateField, SubmitField
from flask import Flask, render_template, make_response
# myplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt

class AnalyzeForm(Form):
    f = DateField('From', [])
    t = DateField('To', [])
    submit = SubmitField('表示')

def analyze(request):
    form = AnalyzeForm(request.form)
    f, t = query(request, 'f'), query(request, 't')
    hasQuery = f is not None and t is not None
    form.f.data = datetime.strptime(f, "%Y-%m-%d").date()
    form.t.data = datetime.strptime(t, "%Y-%m-%d").date()
    return render_template('analyze.html'
            , form=form, f=f, t=t, hasQuery=hasQuery)

def plot(Log, request):
    f, t = query(request, 'f'), query(request, 't')
    logs = Log.query.filter(Log.date>=f).filter(Log.date<=t).all()
    if len(logs) == 0:
        return render_template('404.html'), 404 
    temps = list(map(lambda log:
        0 if log.temp is None else log.temp, logs))
    dates = list(map(lambda log: log.date, logs))
    ecs = list(map(lambda log:
        0 if log.ec is None else log.ec, logs))
    # plot
    plt.figure(1)
    plt.subplot(211)
    plt.plot(dates, temps)
    plt.subplot(212)
    plt.plot(dates, ecs)
    plt.axis([dates[0], dates[len(dates)-1], 0, 1000])
    # make response
    canvas = FigureCanvas(plt.figure(1))
    po = BytesIO()
    canvas.print_png(po)
    response = make_response(po.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

def query(req, name):
    return req.args.get(name)

