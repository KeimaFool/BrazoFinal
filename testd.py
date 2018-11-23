import serial
import time
import sys
from tkinter import *

ser0=127
ser1=127
ser2=210
ser3=100
count=0
save=0
readtxt=0
sync=0
saveB=0
syncB=0

def record(event):
    global save
    global count
    global sync
    
    if save==0:
        button_1.config(text="Stop")
        save=1
        sync=count
        open('prueba.txt', 'w').close()
        print("dead")
    else:
        button_1.config(text="Record")
        save=0
    
def play(event):
    global save
    save=2
    button_1.config(text="Record")
    global readtxt
    readtxt=0

def recordB(event):
    global saveB
    global count
    global syncB
    
    if saveB==0:
        button_3.config(text="Stop")
        saveB=1
        syncB=count
        open('pruebaB.txt', 'w').close()
        print("dead")
    else:
        button_3.config(text="Record")
        saveB=0
    
def playB(event):
    global saveB
    saveB=2
    button_3.config(text="Record")
    global readtxt
    readtxt=0


#COMUNICACION SERIAL DE PIC CON LA CUMPU
ser= serial.Serial(port='COM7',baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout=0)

root = Tk()
root.title="ARM IN ARM"
root.resizable(0,0)
root.geometry("200x300")

label_1= Label(root,text="Sang Woo Shin, Jeffrey Munoz")
label_2=Label(root,text="Entrada:")
label_3=Label(root,text="Servo1:")
label_4=Label(root,text="Servo2:")
label_5=Label(root,text="Servo3:")
label_6=Label(root,text="Servo4:")
label_7=Label(root,text="X")
label_8=Label(root,text="X")
label_9=Label(root,text="X")
label_A=Label(root,text="X")
label_B=Label(root,text="X")
label_C=Label(root,text="Left X:")
label_D=Label(root,text="Left Y:")
label_E=Label(root,text="Right X:")
label_F=Label(root,text="Right Y")
label_G=Label(root,text="X")
label_H=Label(root,text="X")
label_I=Label(root,text="X")
label_J=Label(root,text="Salidas:")
button_1=Button(root, text="Record A")
button_2=Button(root, text="Play A")
button_3=Button(root, text="Record B")
button_4=Button(root, text="Play B")
button_1.bind("<Button-1>",record)
button_2.bind("<Button-1>",play)
button_3.bind("<Button-1>",recordB)
button_4.bind("<Button-1>",playB)

label_1.grid(columnspan=5)
label_2.grid(row=1,sticky=W)
label_3.grid(row=7,sticky=W)
label_4.grid(row=8,sticky=W)
label_5.grid(row=9,sticky=W)
label_6.grid(row=10,sticky=W)
label_7.grid(row=7,column=1)
label_8.grid(row=8,column=1)
label_9.grid(row=9,column=1)
label_A.grid(row=10,column=1)
label_B.grid(row=5,column=1)
label_C.grid(row=2,sticky=W)
label_D.grid(row=3,sticky=W)
label_E.grid(row=4,sticky=W)
label_F.grid(row=5,sticky=W)
label_G.grid(row=2,column=1)
label_H.grid(row=3,column=1)
label_I.grid(row=4,column=1)
label_J.grid(row=6, sticky=W)
button_1.grid(row=11,sticky=E,column=1)
button_2.grid(row=12,sticky=E,column=1)
button_3.grid(row=11,column=2)
button_4.grid(row=12,column=2)

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
    if count>0:
        if recibido1>240 and recibido1<255:
            if count==1:
                ser0=ser0+10
                if ser0>142:
                    ser0=142
            if count==2:
                ser1=ser1+7
                if ser1>140:
                    ser1=140
            if count==3:
                ser2=ser2+10
                if ser2>220: 
                    ser2=220 
            if count==4:
                ser3=ser3+7
                if ser3>120:
                    ser3=120
        if recibido1<25:
            if count==1:
                ser0=ser0-10
                if ser0<30:
                    ser0=30
            if count==2:
                ser1=ser1-7
                if ser1<80:
                    ser1=80
            if count==3:
                ser2=ser2-10
                if ser2<100:
                    ser2=100
            if count==4:
                ser3=ser3-7
                if ser3<50:
                    ser3=50
        if count==1:
            label_B.config(text=str(recibido1))
            recibido1=ser0
            label_7.config(text=str(ser0))
        if count==2:
            label_H.config(text=str(recibido1))
            recibido1=ser1
            label_8.config(text=str(ser1))
        if count==3:
            label_G.config(text=str(recibido1))
            recibido1=ser2
            label_9.config(text=str(ser2))
        if count==4:
            label_I.config(text=str(recibido1))
            recibido1=ser3
            label_A.config(text=str(ser3))
        count=count+1
        if count==5:
            count=1
        
    else:
        if recibido1<10:
            count=4
    if save==1:
        f=open('prueba.txt','a+')
        f.write(str(recibido1)+'\n')
        f.close()
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
            
    if save==2 and count==sync:
        save=3
        print(sync)



    if saveB==1:
        f=open('pruebaB.txt','a+')
        f.write(str(recibido1)+'\n')
        f.close()
    if saveB==3:
        try:
            f=open('pruebaB.txt','r')
            line=f.readlines()[readtxt]
            recibido1=int(line)
            f.close()
            readtxt=readtxt+1
            print(recibido1)
        except:
            saveB=0
            
    if saveB==2 and count==syncB:
        saveB=3
        print(syncB)
    
    ser.write(recibido1.to_bytes(1, byteorder='little')) 
    
        
