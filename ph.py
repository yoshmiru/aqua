from serial import Serial
from time import sleep

def read(ser):
    ser.write(b'PH:')
    return ser.readline().decode('utf-8')


if __name__ == '__main__':
    ser = Serial('/dev/ttyACM0')
    sleep(2)
    print(read(ser))
