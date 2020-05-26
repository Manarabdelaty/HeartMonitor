# -*- coding: utf-8 -*-
"""
Created on Sun May 10 00:28:18 2020

@author: Dell
"""
import serial
import serial.tools.list_ports

class Port:
    
    def __init__(self):
        self.name = ""
        self.ser = ""
        
    def getAllPorts(self):
        # check available com ports
        all_ports = ["COM0"]
        desc = [""]
        com_ports = [port for port in serial.tools.list_ports.comports() if port[2] != 'n/a']

        if len(com_ports) is 0:
            print("No available ports...Are you sure you connecting the USB-UART ? ")
        
        for port in com_ports:
            print ("Port Name: ", port[0], " , Desc.: ", port[1] )
            all_ports.append(port[0])
            desc.append(port[1])
            
        return all_ports, desc
    
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
            #print(f"Received {line}")
        else:
            print("Are you sure you choosing a right port ? ")
            
        return line
    
    def write(self, data):
        data = data.ljust(16, 'H')
        print(data.encode())
        self.ser.write(data.encode())
        print("Data is written")