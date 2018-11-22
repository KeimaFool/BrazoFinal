import serial
import time
import sys

ser0=87
ser1=87
ser2=177
ser3=87
count=0

#COMUNICACION SERIAL DE PIC CON LA CUMPU
ser= serial.Serial(port='COM7',baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout=0)
while 1:
    ser.flushInput()
    ser.flushOutput()
    time.sleep(.01)
    try:
        recibido1=ser.read()
        recibido1=int.from_bytes( recibido1, byteorder='little', signed=False )

    except:
        recibido1=127
        print("[Error]Unable to read")
    if count>0:
        if recibido1>240:
            if count==1:
                ser0=ser0+5
                if ser0>250:
                    ser0=250
            if count==2:
                ser1=ser1+5
                if ser1>250:
                    ser1=250
            if count==3: 
                ser2=ser2+5
                if ser2>177: 
                    ser2=177 
            if count==4:
                ser3=ser3+5
                if ser3>152:
                    ser3=152
        if recibido1<15:
            if count==1:
                ser0=ser0-5
                if ser0<0:
                    ser0=0
            if count==2:
                ser1=ser1-5
                if ser1<32:
                    ser1=32
            if count==3:
                ser2=ser2-5
                if ser2<95:
                    ser2=95 
            if count==4:
                ser3=ser3-5
                if ser3<32:
                    ser3=32
        if count==1:
            recibido1=ser0
            
        if count==2:
            recibido1=ser1
        if count==3:
            recibido1=ser2
        if count==4:
            recibido1=ser3
        count=count+1
        if count==5:
            count=1
        
    else:
        if recibido1>250:
            count=4

    ser.write(recibido1.to_bytes(1, byteorder='little')) 
    
        
