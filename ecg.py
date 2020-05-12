# -*- coding: utf-8 -*-
"""
Created on Fri May  8 23:37:43 2020

@author: Dell
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import time
import serial
import multiprocessing
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
        self.x_vals = []
        self.y_vals = []
        self.index = count()
        
    def read(self, port): 
        value = port.read()
        print(f"Received {value}")
        if value:
            x = next(self.index)
            y = int(value)
            return x, y 
        else:
            return 0, 0
    
    def animate(self, frame, port):
        x, y = self.read(port)
        self.x_vals.append(x)
        self.y_vals.append(y)
        plt.cla()
        plt.plot(self.x_vals, self.y_vals)

        print(f"This is getting called {frame}")

    
    def monitor(self, port):
        self.fig = plt.figure()
        self.ani = animation.FuncAnimation(self.fig, self.animate, fargs=(port,), interval=1)
        plt.show()
    
    def worker(self):
        self.fig = plt.figure()
        print("HELOOOOO")

class Port:
    
    def __init__(self):
        self.name = ""
        self.ser = ""
        
    def getAllPorts(self):
        # check available com ports
        com_ports = [port for port in serial.tools.list_ports.comports() if port[2] != 'n/a']

        if len(com_ports) is 0:
            print("No available ports...Are you sure you connecting the USB-UART ? ")
        
        for port in com_ports:
            print ("Port Name: ", com_ports[0][0], " , Desc.: ", com_ports[0][1] )
        return com_ports
    
    def setPortName(self, name):
        self.name = name
        
    def openPort(self):
        # open selected port
        if self.name:
            print(f"Opening port {self.name}...")
            self.ser = serial.Serial(self.name,
                                     baudrate=115200, # uart baud rate
                                     timeout=0,  # read timeout
                                     parity=serial.PARITY_NONE, # No parity
                                     rtscts=0)
        else:
            print("Set port name first before opening! ")
            
    def closePort(self):
        # open selected port
        if self.name:
            print("Closing Port...")
            self.ser.close()
        else:
            print("Set port name first before opening! ")
    
    def read(self):
        if not self.ser:
            self.openPort()

        if self.ser:
            line = self.ser.readline()
            line = line.decode("utf-8") 
            line = line.replace("\n", "").replace("\r", "")
            print(f"Received {line}")
        else:
            print("Are you sure you choosing a right port ? ")
            
        return line
    
    def write(self, data):
        data = data.ljust(16, 'H')
        print(data.encode())
        self.ser.write(data.encode())
        print("Data is written")

# plotter for monitoring        

port = Port()
sensor = Sensor()

com_ports = port.getAllPorts();

if len(com_ports) != 0: 
    # ask user for which port to use
    port_name =  input("Select com port name : ") 
    port.setPortName(port_name)
    port.openPort()
    # ask for command
    command = input("Enter command: ")
    if command == "no":
        again = False
    else:
        port.write(command)
        if command == "data;":
            sensor.monitor(port)
        
    #port.closePort()
else:
    print("No avaialble ports...")
    
#myplot = Plotter()
#myplot.monitor() 

# sensor read serial values
#sensor = Sensor()
#sensor.selectPort()
#sensor.read()

# re