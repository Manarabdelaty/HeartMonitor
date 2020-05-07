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

from matplotlib import style
style.use('fivethirtyeight')

class Plotter:
    
    def __init__(self):
        self.fig = plt.figure()
        self.x_vals = []
        self.y_vals = []
        
    def animate(self, frame):
        data = pd.read_csv('data.csv')
        x_vals = data.x
        y_vals = data.y
        plt.cla()
        plt.plot(x_vals, y_vals)

        print(f"This is getting called {frame}")

        
    def monitor(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()

class Sensor:
    
    def __init__(self):
        self.com_port = ""
        self.ser = ""
    
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
        # open selected port
        self.ser = serial.Serial(self.myport,
        baudrate=115200, # uart baud rate
        timeout=0,  # read timeout
        parity=serial.PARITY_NONE, # No parity
        rtscts=1)
        
        while True:
            line = self.ser.readline()
            print ('serial closed')
            
        self.ser.close()

# plotter for monitoring        
myplot = Plotter()
myplot.monitor() 

# sensor read serial values
sensor = Sensor()
sensor.selectPort()
sensor.read()
