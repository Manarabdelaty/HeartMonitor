# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import serial
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial.tools.list_ports

import random
from itertools import count

from matplotlib import style
style.use('fivethirtyeight')

class Plotter:
    
    def __init__(self):
        self.fig = plt.figure()
        self.sensor = Sensor()
        self.x_vals = []
        self.y_vals = []
        
    def animate(self, frame):
        #data = pd.read_csv('data.csv')
        #x_vals = data.x
        #y_vals = data.y
        x,y = self.sensor.read()
        self.x_vals.append(x)
        self.y_vals.append(y)
        plt.cla()
        plt.plot(self.x_vals, self.y_vals)

        print(f"This is getting called {frame}")

        
    def monitor(self):
        self.sensor.selectPort()
        self.sensor.open()
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=1)
        plt.show()

class Sensor:
    
    def __init__(self):
        self.com_port = ""
        self.ser = ""
        self.index = count()
    
    def selectPort(self):
        # check available com ports
        com_ports = [port for port in serial.tools.list_ports.comports() if port[2] != 'n/a']

        if len(com_ports) is 0:
            sys.exit("No available ports...Are you sure you connecting the USB-UART ? ")
        
        for port in com_ports:
            print ("Port Name: ", com_ports[0][0], " , Desc.: ", com_ports[0][1] )
       
        # promot the user to select com port
        self.com_port = input("Select com port name : ") 
        print("You chose port: ", self.com_port)

    def read(self): 
        line = self.ser.readline()
        line = line.decode("utf-8") 
        line = line.replace("\n", "").replace("\r", "")
        print(f"Received {line}")
        x = next(self.index)
        y = int(line)                  #random.randint(0, 5)
        return x, y 
    
    def open(self):
        # open selected port
        self.ser = serial.Serial(self.com_port,
        baudrate=115200, # uart baud rate
        timeout=0,  # read timeout
        parity=serial.PARITY_NONE, # No parity
        rtscts=1)
    
    def close(self):
        print ('Closing Serial Port..')
        self.ser.close()

# plotter for monitoring        
myplot = Plotter()
myplot.monitor() 

# sensor read serial values
#sensor = Sensor()
#sensor.selectPort()
#sensor.read()

# re