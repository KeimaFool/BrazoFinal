import serial
import time
import sys
from tkinter import *

ser0=127
ser1=127
ser2=127
ser3=127
count=0
save=0
readtxt=0
sync=0

def record(event):
    global save
    if save==0:
        button_1.config(text="Stop")
        save=1
    else:
        button_1.config(text="Record")
        save=0
    global count
    global sync
    sync=count
def play(event):
    global save
    save=2
    button_1.config(text="Record")
    global readtxt
    readtxt=0


#COMUNICACION SERIAL DE PIC CON LA CUMPU
ser= serial.Serial(port='COM7',baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout=0)

root = Tk()
root.title="ARM IN ARM"
root.resizable(0,0)
root.geometry("200x200")

label_1= Label(root,text="Sang Woo Shin, Jeffrey Munoz")
label_2=Label(root,text="Voltaje de entrada:")
label_3=Label(root,text="Servo1:")
label_4=Label(root,text="Servo2:")
label_5=Label(root,text="Servo3:")
label_6=Label(root,text="Servo4:")
label_7=Label(root,text="X")
label_8=Label(root,text="X")
label_9=Label(root,text="X")
label_A=Label(root,text="X")
label_B=Label(root,text="X")
button_1=Button(root, text="Record")
button_2=Button(root, text="Play")
button_1.bind("<Button-1>",record)
button_2.bind("<Button-1>",play)

label_1.grid(columnspan=5)
label_2.grid(row=1,sticky=W)
label_3.grid(row=2,sticky=W)
label_4.grid(row=3,sticky=W)
label_5.grid(row=4,sticky=W)
label_6.grid(row=5,sticky=W)
label_7.grid(row=2,column=1)
label_8.grid(row=3,column=1)
label_9.grid(row=4,column=1)
label_A.grid(row=5,column=1)
label_B.grid(row=1,column=1)
button_1.grid(columnspan=6)
button_2.grid(columnspan=7)

while 1:
    root.update_idletasks()
    root.update()
    ser.flushInput()
    time.sleep(.01)
    try:
        recibido1=ser.read()
        recibido1=int.from_bytes( recibido1, byteorder='little', signed=False )
        
    except:
        recibido1=127
        print("[Error]Unable to read")
    label_B.config(text=str(recibido1)+"V")
    if count>0:
        if recibido1>230:
            if count==1:
                ser0=ser0+5
                if ser0>250:
                    ser0=250
            if count==2:
                ser1=ser1+5
                if ser1>220:
                    ser1=220
            if count==3:
                ser2=ser2+5
                if ser2>250: 
                    ser2=250 
            if count==4:
                ser3=ser3+5
                if ser3>250:
                    ser3=250
        if recibido1<25:
            if count==1:
                ser0=ser0-5
                if ser0<0:
                    ser0=0
            if count==2:
                ser1=ser1-5
                if ser1<100:
                    ser1=100
            if count==3:
                ser2=ser2-5
                if ser2<0:
                    ser2=0 
            if count==4:
                ser3=ser3-5
                if ser3<0:
                    ser3=0
        if count==1:
            recibido1=ser0
            label_7.config(text=str(ser0))
        if count==2:
            recibido1=ser1
            label_8.config(text=str(ser1))
        if count==3:
            recibido1=ser2
            label_9.config(text=str(ser2))
        if count==4:
            recibido1=ser3
            label_A.config(text=str(ser3))
            print("X")
        count=count+1
        if count==5:
            count=1
        
    else:
        if recibido1>240:
            count=4
    if save==1:
        f=open('prueba.txt','a+')
        f.write(str(recibido1)+'\n')
        f.close()
    if save==2 and count==sync:
        save=3
    if save==3:
        try:
            f=open('prueba.txt','r')
            line=f.readlines()[readtxt]
            recibido1=int(line)
            f.close()
            readtxt=readtxt+1
            print(recibido1)
        except:
            save=0
            open('prueba.txt', 'w').close()
            print("dead")
    
    ser.write(recibido1.to_bytes(1, byteorder='little')) 
    
        
