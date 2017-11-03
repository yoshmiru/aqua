#!/usr/bin/env python
from serial import Serial
from time import sleep

def feed(ser):
    normal = 60
    feed = 180
    ser.write(bytearray('FEED:{}'.format(feed), 'utf-8'))
    print(ser.readline())
    sleep(0.5)
    ser.write(bytearray('FEED:{}'.format(normal), 'utf-8'))
    print(ser.readline())
    sleep(0.5)

if __name__ == '__main__':
    ser = Serial('/dev/ttyACM0')
    sleep(2)
    feed(ser)

