from flask import render_template, request

def cam():
    return render_template('index.html')

def cam_ctl(ser, x, y):
    print('{}, {}'.format(x, y))
    ser.write(bytearray('CAM:{},{}'.format(x, y), 'utf-8'))
    print(ser.readline())
