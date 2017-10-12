from flask import render_template, request

def cam():
    return render_template('index.html')

def cam_ctl(x, y):
    print('{}, {}'.format(x, y))
