import serial
import time
class Packet:
    def __init__(self, forwards, backards, left, right):
        self.forwards = forwards
        self.backwards = backards
        self.left = left
        self.right = right

    def send(self):
        arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
        arduino.write(bytes(self, 'utf-8'))
        print(arduino.readline().decode('utf-8').rstrip())