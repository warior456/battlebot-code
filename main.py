from tkinter import *
from tkinter import ttk
import serial
import time

root = Tk()
root.geometry("550x300")  # widthxheight
frame = ttk.Frame(root, padding=10)
frame.grid()
arduino = serial.Serial(port='/dev/ttyACM1', baudrate=9600, timeout=.1)

speedvar = 1

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    return

def read():
    data = arduino.readline().decode('utf-8').rstrip()
    return data

def forward():
    write("forward")
    time.sleep(0.15)
    print(read() + '\n' + read())
    return


def backward():
    write("backwards")
    time.sleep(0.15)
    print(read() + '\n' + read())
    return


def left():
    write("left")
    time.sleep(0.15)
    print(read() + '\n' + read())
    return


def right():
    write("right")
    time.sleep(0.15)
    print(read() + '\n' + read())
    return


def ping():

    ping = "ping["
    ping += ping_val.get()
    ping += "]"
    write(ping)
    pong = read()
    pingLabel.configure(text= "pong")

    return

def speed(speedvar):


    return


# buttons

ttk.Button(frame, text="forwards", command=forward).grid(column=5, row=0)
ttk.Button(frame, text="backwards", command=backward).grid(column=5, row=3)
ttk.Button(frame, text="left", command=left).grid(column=4, row=2)
ttk.Button(frame, text="right", command=right).grid(column=6, row=2)


ttk.Button(frame, text="ok",command=lambda : ping()).grid(column=1, row=4)

#labels
ttk.Label(frame, text= "ping").grid(column=0, row=3)
pingLabel = ttk.Label(frame, text= "not yet pinged").grid(column=0, row=5)
ttk.Label(frame, text= "speed").grid(column=0, row=0)
speedLabel = ttk.Label(frame, text= speedvar).grid(column=0, row=2)

#sliders

ttk.Scale(frame, length= 100, variable = speedvar).grid(column=0, row=1)

ping_val = StringVar()
ttk.Entry(frame, textvariable=ping_val).grid(column=0, row=4)

ttk.Button(frame, text="Quit", command=root.destroy).grid(column=5, row=10)

root.mainloop()
#print(speedvar)
#print(pa.forwards + pa.backwards + pa.left + pa.right)
#speedLabel.configure(text= speedvar)
