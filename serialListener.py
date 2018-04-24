# -*- coding: utf-8 -*-
import serial
import sys

# create serial object
serial_port = sys.argv[1]
serial_baudrate = int(sys.argv[2])
callback_timeout = int(sys.argv[3])
ser = serial.Serial(serial_port, serial_baudrate, timeout=1)

ser.write("start")

while True:    
    command = ser.readline()
    print command
