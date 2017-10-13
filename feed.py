from serial import Serial
from time import sleep

ser = Serial('/dev/ttyACM0')
sleep(2)
ser.write(b'FEED:180')
print(ser.readline())
sleep(0.5)
ser.write(b'FEED:175')
print(ser.readline())
sleep(0.5)
ser.write(b'FEED:180')
print(ser.readline())
sleep(0.5)
ser.write(b'FEED:175')
print(ser.readline())
sleep(0.5)
ser.write(b'FEED:180')
print(ser.readline())
sleep(2)
ser.write(b'FEED:100')
print(ser.readline())
