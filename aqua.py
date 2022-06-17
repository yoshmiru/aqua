from datetime import datetime 
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from functools import reduce
from math import sqrt, pow
from serial import Serial
from threading import Timer
from time import sleep
from RPi import GPIO

# local
from aqua_db import setup as setup_db
from aqua_log import setup as setup_log
from handler.analyze import analyze as h_analyze#, plot as h_plot
from handler.cam import cam as h_cam, cam_ctl as h_cam_ctl

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
led = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
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

class FeedLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date=db.Column(db.DateTime())
    def __init__(self):
        self.date = datetime.now()
    def __repr__(self):
        return '<Feed at {:%Y-%m-%d %H:%M:%S}>'.format(self.date)

def to_temp(v):
    try:
        return -1481.96 + sqrt((2.1962 * pow(10, 6)) + ((1.8639-v)/(3.88*pow(10, -6))))
    except ValueError as e:
        app.logger.error('ValueError on `{}`'.format(v))
        app.logger.error(e)

def read_temp():
    ser.write(b'T')
    raw = 0#ser.readline().decode('utf-8')
    mv = 0#ser.readline().decode('utf-8')
    try:
        v = float(mv)
        temp = to_temp(v)
        app.logger.debug('raw: {}, vo: {}, temp: {}'.format(raw, v, temp))
        return temp
    except Exception as e:
        app.logger.error('Could not read temp: `{}`'.format(mv))
        app.logger.error(e)
        return None

def read_ec():
    ser.write(b'E')
    v = 0#ser.readline().decode('utf-8')
    try:
        app.logger.debug('discharge: {}'.format(v))
        return float(v)
    except ValueError as e:
        app.logger.error('ValueError on `{}`'.format(v))
        app.logger.error(e)

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

#@app.route('/plot.png')
#def plot():
#    return h_plot(Log, request)

@socketio.on('led ctl')
def handle_led_ctl(on):
    if on:
        GPIO.output(led, GPIO.HIGH)
    else:
        GPIO.output(led, GPIO.LOW)

@socketio.on('servo ctl')
def handle_servo_ctl():
    interval = 60 * 60
    now = datetime.now()
    lastFeed = FeedLog.query.order_by(FeedLog.date.desc()).first()
    last = interval + 1 if lastFeed is None else lastFeed.date
    delta = now - lastFeed.date
    if delta.seconds < interval:
        emit('alert', 'あげ過ぎ注意!')
        emit('feed info', '{:%H:%M}'.format(last))
    else:
        ser.write(b'S')
        ser.write(b'165')
        sleep(2)
        ser.write(b'S')
        ser.write(b'110')
        emit('feed info', '{:%H:%M}'.format(now))
        app.logger.info('feed from %s', request.remote_addr)
        db.session.add(FeedLog())
        db.session.commit()

@socketio.on('read temp')
def handle_read_temp():
    return read_temp()

@socketio.on('read ec')
def handle_read_ec():
    ec = read_ec()
    app.logger.debug('ec: {}'.format(ec))
    return ec

@socketio.on('cam ctl')
def cam_ctl(x, y):
    h_cam_ctl(ser, x, y)

#store_log()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
