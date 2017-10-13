from datetime import datetime, date, timedelta
from io import BytesIO
# flask
from wtforms import Form, DateField, SubmitField
from flask import Flask, render_template, make_response, send_file
# myplotlib
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib import pyplot as plt

class AnalyzeForm(Form):
    f = DateField('From', [])
    t = DateField('To', [])
    submit = SubmitField('表示')

def analyze(Log, request):
    fmt = '%Y-%m-%d'
    form = AnalyzeForm(request.form)
    f, t = query(request, 'f'), query(request, 't')
    hasQuery = f is not None and t is not None
    _t = None if t is None else (datetime.strptime(t, fmt) + timedelta(days=1)).date()
    logs = list(map(none2zero, Log.query \
              .filter(Log.date>=f) \
              .filter(Log.date<=_t) \
              .all())) if hasQuery else []
    if hasQuery:
        form.f.data = datetime.strptime(f, fmt).date()
        form.t.data = datetime.strptime(t, fmt).date()
    return render_template('analyze.html'
            , form=form, logs=logs)

def none2zero(log):
    temp = 0 if log.temp is None else log.temp
    ec = 0 if log.ec is None else log.ec
    return {'temp': temp, 'ec': ec, 'date': log.date}


#def plot(Log, request):
#    f, t = query(request, 'f'), query(request, 't')
#    logs = Log.query.filter(Log.date>=f).filter(Log.date<=t).all()
#    if len(logs) == 0:
#        return send_file('static/img/no_data.png', 'image/png')
#    temps = list(map(lambda log:
#        0 if log.temp is None else log.temp, logs))
#    ecs = list(map(lambda log:
#        0 if log.ec is None else log.ec, logs))
#    dates = list(map(lambda log: log.date, logs))
#    # plot
#    font = {'fontname': 'Mona'}
#    plt.figure(1)
#    plt.subplot(211)
#    plt.xlabel('時間', **font)
#    plt.ylabel('温度', **font)
#    plt.plot(dates, temps)
#    plt.axis([dates[0], dates[len(dates)-1], -5, 40])
#    plt.subplot(212)
#    plt.xlabel('時間', **font)
#    plt.ylabel('電気伝導度 アナログ入力(0-1024)', **font)
#    plt.plot(dates, ecs)
#    plt.axis([dates[0], dates[len(dates)-1], 500, 700])
#    # adjust layout
#    plt.tight_layout()
#    # make response
#    canvas = FigureCanvas(plt.figure(1))
#    po = BytesIO()
#    canvas.print_png(po)
#    response = make_response(po.getvalue())
#    response.headers['Content-Type'] = 'image/png'
#    return response

def query(req, name):
    return req.args.get(name)

