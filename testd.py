import serial
import time
import sys

#COMUNICACION SERIAL DE PIC CON LA CUMPU
ser= serial.Serial(port='COM7',baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout=0)
while 1:
    ser.flushInput()
    ser.flushOutput()
    time.sleep(.1)
    try:
        recibido1=ser.read()
        recibido1=int.from_bytes( recibido1, byteorder='little', signed=False )
        
    except:
        recibido1=255
        print("[Error]Unable to read")

    ser.write(recibido1.to_bytes(1, byteorder='little'))
    print(recibido1)
        
