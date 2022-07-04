from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("500x200")  # widthxheight
frame = ttk.Frame(root, padding=10)
frame.grid()


def forward():
    return


def backward():
    return


def left():
    return


def right():
    return


def ping():
    pong = "pong["
    pong += ping_val.get()
    pong += "]"
    ttk.Label(frame, text= pong).grid(column=0, row=5)
    return

def speed(speed):
    ttk.Label(frame, text= speed).grid(column=0, row=1)
    return


# buttons

ttk.Button(frame, text="forwards", command=forward).grid(column=5, row=0)
ttk.Button(frame, text="backwards", command=backward).grid(column=5, row=3)
ttk.Button(frame, text="left", command=left).grid(column=4, row=2)
ttk.Button(frame, text="right", command=right).grid(column=6, row=2)


ttk.Button(frame, text="ok",command=lambda : ping()).grid(column=1, row=4)

#labels
ttk.Label(frame, text= "ping").grid(column=0, row=3)

ttk.Label(frame, text= "speed").grid(column=0, row=0)

#sliders

ttk.Scale(frame, length= 100, variable = lambda : speed()).grid(column=0, row=1)

ping_val = StringVar()
ttk.Entry(frame, textvariable=ping_val).grid(column=0, row=4)

ttk.Button(frame, text="Quit", command=root.destroy).grid(column=5, row=10)

root.mainloop()
