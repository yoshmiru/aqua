from flask import Flask, request
# local
from aqua_db import setup as setup_db
from aqua_log import setup as setup_log
from handler.analyze import analyze as h_analyze, plot as h_plot

app = Flask(__name__)
db = setup_db(app)
logger = setup_log(app)

# defining models
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float)
    ec = db.Column(db.Float)
    date = db.Column(db.DateTime)
    def __init__(self, temp, ec):
        self.temp = temp
        self.ec = ec
        self.date = datetime.now()
    def __repr__(self):
        return '<Log {}:{} at {:%Y-%m-%d %H:%M:%S}>'\
                .format(self.temp, self.ec, self.date)

@app.route('/')
def index():
    return h_analyze(Log, request)

@app.route('/plot.png')
def plot():
    return h_plot(Log, request)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
