from serial import Serial
from time import sleep

ser = Serial('/dev/ttyACM0')
sleep(2)
ser.write(b'S')
ser.write(b'165')
sleep(2)
ser.write(b'S')
ser.write(b'100')
