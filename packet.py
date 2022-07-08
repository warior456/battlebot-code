import serial
import time

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

# vooruit, achteruit, links, rechts, speed
def send_packet(keyList):
    packet_data = true_false(keyList['z'])
    packet_data += true_false(keyList['s'])
    packet_data += true_false(keyList['q'])
    packet_data += true_false(keyList['d'])
    packet_data += true_false(keyList['speed'])
    return send_raw(packet_data)


def send_raw(packet_data):
    print(packet_data)
    write(packet_data)
    # read()
    return read()


def send_command(packet_data):
    print(packet_data)
    write(packet_data)
    read()
    time.sleep(0.25)
    write(packet_data)
    read()
    time.sleep(0.25)
    return read()


def true_false(x):
    if x == False:
        x = 0
    if x == True:
        x = 1
    return str(x)


def write(x):
    arduino.write(bytes(x, 'utf-8'))
    return


def read():
    data = arduino.readline().decode('utf-8').rstrip()
    # data = "placeholder"
    return data
