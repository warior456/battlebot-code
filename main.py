import serial
from tkinter import *
from tkinter import ttk
import time
import packet
from copy import deepcopy

root = Tk()
root.title('controller gui')

root.geometry("550x300")  # widthxheight
root.resizable(width=False, height=False)
frame = ttk.Frame(root, padding=10)
frame.grid()

speed_var = "230"
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
    global keyList, keyChange, timerhandle, resend_var

    if keyChange != keyList:
        keyChange = deepcopy(keyList)
        resend_var = 2
    # print(keyList['speed'])
    # print(speed_var)
    packet.send_packet(keyList)
    # if resend_var >= 1:
    #
    #     print(resend_var)
    #     resend_var -= 1
    #     print(resend_var)

    timerhandle = root.after(250, onTimer)


# def forward(keyList):
#     packet.button_write(keyList, 'z', button_time)
#     return
#
#
# def backward(keyList):
#     packet.button_write(keyList, 's', button_time)
#     return
#
#
# def left(keyList):
#     packet.button_write(keyList, 'q', button_time)
#     return
#
#
# def right(keyList):
#     packet.button_write(keyList, 'd', button_time)
#     return


def send_command():
    ping = ping_val.get()
    ping_entry.config(state=DISABLED)
    command_send_btn.config(state=DISABLED)
    pong = packet.send_raw(ping)

    ping_resp.config(text=pong)
    ping_entry.config(state=NORMAL)
    command_send_btn.config(state=NORMAL)

    return

def speed(speed_var):
    global speed_msg
    speed_msg = "speed: "
    keyList['speed'] = speed_var
    speed_msg += speed_var
    speed_label.config(text=speed_msg)
    return


# buttons
# ttk.Button(frame, text="forwards", command=forward(keyList)).grid(column=1, row=0)
# ttk.Button(frame, text="backwards", command=backward(keyList)).grid(column=1, row=2)
# ttk.Button(frame, text="left", command=left(keyList)).grid(column=0, row=1)
# ttk.Button(frame, text="right", command=right(keyList)).grid(column=2, row=1)
command_send_btn = Button(frame, text="ok", command=send_command)
command_send_btn.grid(column=4, row=1)

# labels
ping_label = Label(frame, text="Send a command")
ping_label.grid(column=3, row=0)
ping_resp = Label(frame, text="No commands sent yet")
ping_resp.grid(column=3, row=2)

speed_label = Label(frame, text="speed: ")
speed_label.grid(column=0, row=3)

# sliders
speed_scale = Scale(frame, length=100, orient=VERTICAL, command=speed, from_=50, to=255)
speed_scale.grid(column=0, row=4)
speed_scale.set(speed_var)

#
ping_val = StringVar()
ping_entry = Entry(frame, textvariable=ping_val, state=DISABLED)
ping_entry.grid(column=3, row=1)

# keybinds
root.bind("<KeyPress>", onKeyDown)
root.bind("<KeyRelease>", onKeyUp)
timerhandle = root.after(250,onTimer)

root.mainloop()

# print(pa.forwards + pa.backwards + pa.left + pa.right)
# speedLabel.configure(text= speed_var)
