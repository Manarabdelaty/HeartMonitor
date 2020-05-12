# -*- coding: utf-8 -*-
"""
Created on Fri May  8 06:39:06 2020

@author: Dell
"""

import tkinter as tk
from PIL import Image, ImageTk
import sys
sys.path.append('F:/Epilogue/HeartMonitor/')
from port import Port
 
def change(*args):
    print("Selected port: ", default.get())

def selectBtnClick():
    port.setPortName(default.get())
    try:
        port.openPort()
        print("Port opened successfuly!")
    except:
        print("Failed to open port...")

def setBtnClick():
    pass

def bpmBtnClick():
    pass

def dataBtnClick():
    pass

window = tk.Tk()

frame0 =  tk.Frame(master=window, width=200, height=0.5, bg="gray95")
frame0.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

load = Image.open("logo.png")
render = ImageTk.PhotoImage(load.resize((200, 80)))
img = tk.Label(image=render)
img.image = render
img.pack(anchor="n",side=tk.TOP, expand=True)

frame1 = tk.Frame(master=window, width=200, height=100, bg="gray95")
frame1.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

# dropdown menu
port = Port()
options, desc = port.getAllPorts()

default = tk.StringVar(window)
default.set(options[0])
default.trace("w", change)
dropDownMenu = tk.OptionMenu(frame1, default, *options)
dropDownMenu.configure(width=50, height=2)
dropDownMenu.pack(anchor="n", side=tk.LEFT, expand=True)

# select button
portButton = tk.Button(frame1, width=20, height=2, text="Select", fg="red", command=selectBtnClick)
portButton.pack(anchor="n",side=tk.RIGHT, expand=True)

frame2 = tk.Frame(master=window, width=100, height=100, bg="gray95")
frame2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

# sample rate
label = tk.Label(frame2, text="Sample rate SPS")
entry = tk.Entry(frame2, fg="yellow", bg="red", width=50)
label.pack(side=tk.TOP, expand=True)
entry.pack(side=tk.LEFT, expand=True)

# set button
rateButton = tk.Button(frame2, width=20, height=2, text="Set", fg="red", command=setBtnClick)
rateButton.pack(side=tk.RIGHT, expand=True)

frame3 = tk.Frame(master=window, width=50,height=400, bg="gray95")
frame3.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
# bpm button
bpmButton = tk.Button(frame3, width=20, height=2, text="BPM", fg="red", command=bpmBtnClick)
bpmButton.pack(side=tk.TOP, expand=True)

rate = tk.Label(frame3, text="?? bpm", fg="red")
rate.pack(anchor="s",side=tk.BOTTOM, expand=True)

frame4 = tk.Frame(master=window, width=50,height=500, bg="blue")
frame4.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

dataButton = tk.Button(frame4, width=20, text="Collect Data", fg="red", command=dataBtnClick)
dataButton.pack(anchor="ne",side=tk.RIGHT, expand=True)

window.mainloop()
