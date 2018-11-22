from tkinter import*
import serial, time


#Click
def click():
    entered_text=textentry.get()
    f=open("prueba.txt","a+")
    f.write(entered_text+"\n")
    f.close()

    textentry.delete(0,'end')


window=Tk()
window.title("Mini proyecto")
window.configure(background="black")

window.resizable(0,0)
window.geometry("600x300")

Label(window, text="Jeffrey Munoz, 17323",bg="black",fg="white", font="times").grid(row=0,column=0, sticky=W)
Label(window, text="Sang Woo Shin, 15372",bg="black",fg="white", font="times").grid(row=1,column=0, sticky=W)      

Label(window, text="Voltaje detectado:",bg="black",fg="white", font="times").grid(row=3,column=1, sticky=W)

Label(window, text="Angulo para servo:",bg="black",fg="white", font="times").grid(row=4,column=1, sticky=W)

textentry=Entry(window,width=10,bg="white")
textentry.grid(row=4,column=2,sticky=W)

Button(window,text="SUBMIT", width=6,command=click).grid(row=5,column=2,sticky=W)
#Button(window,text="CLEAR", width=6,command=clear).grid(row=6,column=2,sticky=W)


