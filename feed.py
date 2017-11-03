#!/usr/bin/env python
from serial import Serial
from time import sleep

def feed(ser):
    ser.write(b'FEED:180')
    print(ser.readline())
    ser.write(b'FEED:100')
    print(ser.readline())


if __name__ == '__main__':
    ser = Serial('/dev/ttyACM0')
    sleep(2)
    feed(ser)
    #feed(ser)
    #feed(ser)
