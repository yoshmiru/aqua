from flask import Flask
from flask_socketio import SocketIO
from handler.cam import cam as h_cam, cam_ctl as h_cam_ctl

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return h_cam()

# dummy
@app.route('/analyze')
def analyze():
    return None

@socketio.on('cam ctl')
def cam_ctl(x, y):
    h_cam_ctl(x, y)
