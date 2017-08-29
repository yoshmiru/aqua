from datetime import datetime 
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from functools import reduce
from gpiozero import LED
from math import sqrt, pow
from serial import Serial
from threading import Timer
from time import sleep
# local
from aqua_db import setup as setup_db
from aqua_log import setup as setup_log
from handler.analyze import analyze as h_analyze, plot as h_plot

def logHandler():
    handler = RotatingFileHandler('aqua.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    return handler

app = Flask(__name__)
# enable socketio
socketio = SocketIO(app)
# db settings
db = setup_db(app)
# logger settings
logger = setup_log(app)
# GPIO settings
led = LED(2)
ser = Serial('/dev/ttyACM0')
sleep(2)
#
# defining models
#
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
        return '<Log {}:{} at {:%Y-%m-%d %H:%M:%S}>'.format(self.temp, self.ec, self.date)

def to_temp(v):
    try:
        return -1481.96 + sqrt((2.1962 * pow(10, 6)) + ((1.8639-v)/(3.88*pow(10, -6))))
    except ValueError:
        app.logger.error('ValueError on `{}`'.format(v))

def read_temp():
    ser.write(b'T')
    mv = ser.readline()
    try:
        v = float(mv)
        return to_temp(v)
    except Exception as e:
        app.logger.error('Could not read temp: `{}`'.format(mv))
        print(e)
        app.logger.error(e)
        return None

def read_ec():
    ser.write(b'E')
    app.logger.debug('discharge: %f', float(ser.readline()))
    return float(ser.readline())

def store_log():
    db.session.add(Log(read_temp(), read_ec()))
    db.session.commit()
    Timer(60, store_log).start()

@app.route('/')
def index():
    app.logger.info('access from %s', request.remote_addr)
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    return h_analyze(Log, request)

@app.route('/plot.png')
def plot():
    return h_plot(Log, request)

@socketio.on('led ctl')
def handle_led_ctl(on):
    if on:
        led.on()
    else:
        led.off()

feeds = [datetime.now()]
@socketio.on('servo ctl')
def handle_servo_ctl():
    now = datetime.now()
    last = feeds.pop()
    delta = now - last
    if delta.seconds < 60 * 60:
        feeds.append(last)
        emit('alert', 'あげ過ぎ注意!')
        emit('feed info', '{:%H:%M}'.format(last))
    else:
        feeds.append(now)
        emit('feed info', '{:%H:%M}'.format(now))
        feeds.append(now)
        app.logger.info('feed from %s', request.remote_addr)
        ser.write(b'S')
        ser.write(b'165')
        sleep(2)
        ser.write(b'S')
        ser.write(b'110')

temps = []
@socketio.on('read temp')
def handle_read_temp():
    temp = read_temp()
    if temp is not None:
        temps.append(temp)
        app.logger.debug('temp: {}'.format(temp))
        if (len(temps) > 10):
            temps.pop(0)
    return reduce(lambda a, b: a + b, temps) / len(temps)


@socketio.on('read ec')
def handle_read_ec():
    ec = read_ec()
    app.logger.debug('ec: %f', ec)
    return ec

store_log()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
