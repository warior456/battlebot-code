import serial
from tkinter import *
from tkinter import ttk
import time
from copy import deepcopy

root = Tk()
root.title('controller gui')

root.geometry("550x300")  # widthxheight
root.resizable(width=False, height=False)
frame = ttk.Frame(root, padding=10)
frame.grid()
arduino = serial.Serial(port='/dev/ttyACM1', baudrate=9600, timeout=.1)

speed_var = "1"
speed_msg = "speed: "
speed_msg += speed_var

keyDown = False
lastKey = "none"
keyList = {'z': False, 's': False, 'q': False, 'd': False, 'speed': speed_var}  #vooruit, achteruit, links, rechts, speed
keyChange = ""


def onKeyDown(event):
    global keyDown, lastKey, keyList
    if event.char in keyList and keyList[event.char] != True:
        keyList[event.char] = True
    keyDown = True
    lastKey = event.char


def onKeyUp(event):
    global keyDown
    if event.char in keyList and keyList[event.char] == True:
        keyList[event.char] = False
    if len(keyList) == 0:
        keyDown = False


def onTimer():
    global keyList, keyChange, timerhandle

    if keyChange != keyList:
        keyChange = deepcopy(keyList)
    print(str(keyList))

    print(read())
    timerhandle = root.after(800, onTimer)


def write(x):
    arduino.write(bytes(x, 'utf-8'))
    return


def read():
    data = arduino.readline().decode('utf-8').rstrip()
    # data = "placeholder"
    return data


# def forward(keyList):
#     write(keyList)
#     time.sleep(0.15)
#     print(read() + read())
#     return
#
#
# def backward(keyList):
#     write(keyList)
#     time.sleep(0.15)
#     print(read() + read())
#     return
#
#
# def left(keyList):
#     write(keyList)
#     time.sleep(0.15)
#     print(read() + read())
#     return
#
#
# def right(keyList):
#     keyList['d'] = True
#     write(keyList)
#     time.sleep(0.15)
#     print(read() + read())
#     return


def send_command():
    ping = ping_val.get()
    write(ping)
    time.sleep(0.20)
    pong = read()
    ping_resp.config(text=pong)
    return


def speed(speed_var):
    global speed_msg
    speed_msg = "speed: "
    speed_msg += speed_var
    speed_label.config(text=speed_msg)

    return


# buttons
# ttk.Button(frame, text="forwards", command=forward).grid(column=1, row=0)
# ttk.Button(frame, text="backwards", command=backward).grid(column=1, row=2)
# ttk.Button(frame, text="left", command=left).grid(column=0, row=1)
# ttk.Button(frame, text="right", command=right).grid(column=2, row=1)
ttk.Button(frame, text="ok", command=send_command).grid(column=4, row=1)

# labels
ping_label = Label(frame, text="Send a command")
ping_label.grid(column=3, row=0)
ping_resp = Label(frame, text="No commands sent yet")
ping_resp.grid(column=3, row=2)

speed_label = Label(frame, text=speed)
speed_label.grid(column=0, row=3)

# sliders
speed_scale = Scale(frame, length=100, orient=VERTICAL, command=speed)
speed_scale.grid(column=0, row=4)
speed_scale.set(speed_var)

#
ping_val = StringVar()
ping_entry = Entry(frame, textvariable=ping_val)
ping_entry.grid(column=3, row=1)

# keybinds
root.bind("<KeyPress>", onKeyDown)
root.bind("<KeyRelease>", onKeyUp)
# timerhandle = root.after(800,onTimer)

root.mainloop()

# print(pa.forwards + pa.backwards + pa.left + pa.right)
# speedLabel.configure(text= speed_var)
