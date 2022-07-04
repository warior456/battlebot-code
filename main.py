# import serial
from tkinter import *
from tkinter import ttk
import time

root = Tk()
root.title('controller gui')
root.geometry("550x300")  # widthxheight
frame = ttk.Frame(root, padding=10)
frame.grid()
# arduino = serial.Serial(port='/dev/ttyACM1', baudrate=9600, timeout=.1)


speed_var = "1"
speed_msg = "speed: "
speed_msg += speed_var



def write(x):
    # arduino.write(bytes(x, 'utf-8'))
    print(x)
    return


def read():
    # data = arduino.readline().decode('utf-8').rstrip()
    data = "placeholder"
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
    ping_resp.config(text=pong)
    return


def speed():
    global  speed_msg
    speed_msg = "speed: "
    speed_msg += speed_var
    speed_scale.config(label= speed_msg)

    return


# buttons
ttk.Button(frame, text="forwards", command=forward).grid(column=1, row=0)
ttk.Button(frame, text="backwards", command=backward).grid(column=1, row=2)
ttk.Button(frame, text="left", command=left).grid(column=0, row=1)
ttk.Button(frame, text="right", command=right).grid(column=2, row=1)
ttk.Button(frame, text="ok", command=ping).grid(column=1, row=4)

# labels
ping_label = Label(frame, text="ping")
ping_label.grid(column=0, row=3)

ping_resp = Label(frame, text="not yet pinged")
ping_resp.grid(column=0, row=5)



# sliders

speed_scale = Scale(frame, length=100,label=speed_msg, orient=HORIZONTAL)
speed_scale.grid(column=5, row=6)
speed_scale.set(speed_var)
print(speed_scale.get())

ping_val = StringVar()
ping_entry = Entry(frame, textvariable=ping_val)
ping_entry.grid(column=0, row=4)

speed()
root.mainloop()

# print(speed_var)
# print(pa.forwards + pa.backwards + pa.left + pa.right)
# speedLabel.configure(text= speed_var)
