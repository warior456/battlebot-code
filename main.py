from tkinter import *
from tkinter import ttk
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
keyList = {'z': False, 's': False, 'q': False, 'd': False,
           'speed': speed_var}  # vooruit, achteruit, links, rechts, speed
keyChange = ""

packet_delay = 250
off = False


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
    if off == False:
        if keyChange != keyList:
            keyChange = deepcopy(keyList)
            resend_var = 2
        packet.send_packet(keyList)

    timerhandle = root.after(packet_delay, onTimer)


def send_command():
    ping = command_val.get()
    command_entry.config(state=DISABLED)
    command_send_btn.config(state=DISABLED)
    packet.read()
    pong = packet.send_command(ping)
    print(pong)
    ping_resp.config(text=pong)
    command_entry.config(state=NORMAL)
    command_send_btn.config(state=NORMAL)
    return


def on_off():
    global off
    if off == True:
        on_off_btn.config(text="turn control packets off")
        command_entry.config(state=DISABLED)
        command_send_btn.config(state=DISABLED)
        off = False
    elif off == False:
        on_off_btn.config(text="turn control packets on")
        command_entry.config(state=NORMAL)
        command_send_btn.config(state=NORMAL)
        off = True


def motor_speed(speed_var):
    speed_msg = "motor speed: "
    keyList['speed'] = speed_var
    speed_msg += speed_var
    motor_speed_label.config(text=speed_msg)


def packet_speed(delay):
    global packet_delay
    packet_delay = delay
    packet_speed_label.config(text='packet delay: ' + packet_delay + 'ms')
    return


# buttons
on_off_btn = Button(frame, text="turn control packets off", command=on_off)
on_off_btn.grid(column=2, row=1)
command_send_btn = Button(frame, text="ok", command=send_command, state=DISABLED)
command_send_btn.grid(column=1, row=1)

# labels
ping_label = Label(frame, text="Send a command")
ping_label.grid(column=0, row=0)
ping_resp = Label(frame, text="No commands sent yet\n")
ping_resp.grid(column=0, row=2)

motor_speed_label = Label(frame, text="motor speed: ")
motor_speed_label.grid(column=0, row=3)

packet_speed_label = Label(frame, text="packet delay: ")
packet_speed_label.grid(column=2, row=3)

# sliders
packet_speed_scale = Scale(frame, length=100, orient=VERTICAL, command=packet_speed, from_=150, to=1000)
packet_speed_scale.grid(column=2, row=4)
packet_speed_scale.set(packet_delay)
motor_speed_scale = Scale(frame, length=100, orient=VERTICAL, command=motor_speed, from_=50, to=255)
motor_speed_scale.grid(column=0, row=4)
motor_speed_scale.set(speed_var)

# text
command_val = StringVar()
command_entry = Entry(frame, textvariable=command_val, state=DISABLED)
command_entry.grid(column=0, row=1)

# keybinds
root.bind("<KeyPress>", onKeyDown)
root.bind("<KeyRelease>", onKeyUp)
timerhandle = root.after(packet_delay, onTimer)

root.mainloop()
