# -*- coding: utf-8 -*-
import serial
import sys
import datetime


# create serial object
serial_port = sys.argv[1]
serial_baudrate = int(sys.argv[2])
#callback_timeout = int(sys.argv[3])

filename = "data/"+ datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S")
f = open(filename+".csv", "w")

ser = serial.Serial(serial_port, serial_baudrate, timeout=32)
#ser.write("start")

f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))#[:-3]
f.write("\n")
while True:    
    data = ser.readline()
    f.write(data)
    #f.flush()
f.close()
