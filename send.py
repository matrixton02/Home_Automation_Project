import serial
import time
arduino = serial.Serial(port='COM10', baudrate=9600, timeout=.1)
def write_read(x):
    x=str(x)
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

def control(value):
    write_read(value)