# -*- coding: utf-8 -*-
"""
Created on Sun May 10 19:23:56 2020

@author: Dell
"""
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
sys.path.append('F:/Epilogue/HeartMonitor/')
from port import Port
from itertools import count
import random

style.use("ggplot")

port = Port()

def change(default):
    print("Selected port: ", default.get())

def selectBtnClick(port, default):
    port.setPortName(default.get())
    try:
        port.openPort()
        print("Port opened successfuly!")
    except:
        print("Failed to open port...")

def setBtnClick(port, entry):
    rate = entry.get()
    if rate:
        command = f"rate={rate};"
        try:
            port.write(command)
        except:
            print("failed to write to port... you sure it is opened ? ")
    else:
        print("Feild is empty!!")


def bpmBtnClick(port):
    command = "hbpm;"
    try:
        port.write(command)
    except:
        print("failed to write to port... you sure it is opened ? ")
        
def dataBtnClick(port):
    command = "data;"
    try:
        port.write(command)
    except:
        print("failed to write to port... you sure it is opened ? ")

class Heart(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="icon.png")
        tk.Tk.wm_title(self, "ECG Monitor")
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand= True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, DataPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont, caller=None):
        if caller == DataPage:
            self.frames[DataPage].stop()
        elif cont == DataPage:
            self.frames[cont].start()
            
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=200, height=200, bg="gray95")        
        
        load = Image.open("logo.png")
        render = ImageTk.PhotoImage(load.resize((200, 80)))
        img = tk.Label(image=render)
        img.image = render
        img.pack(anchor="n",side=tk.TOP, expand=True)
        
        # dropdown menu
        options, desc = port.getAllPorts()

        default = tk.StringVar(parent)
        default.set(options[0])
        default.trace("w", lambda x,y,z: change(default))
        dropDownMenu = tk.OptionMenu(self, default, *options)
        dropDownMenu.configure(width=70, height=2)
        dropDownMenu.pack(anchor="nw", side=tk.LEFT, expand=True)
        
        # select button
        portButton = tk.Button(self, width=30, height=2, text="Select", fg="red",
                               command= lambda: selectBtnClick(port, default))
        portButton.pack(anchor="ne",side=tk.RIGHT, expand=True)
        #portButton.grid(row=1, column=2, columnspan=2)
        
        # sample rate
        label = tk.Label(self, text="Sample rate SPS")
        entry = tk.Entry(self, fg="yellow", bg="red", width=50)
        label.pack(side=tk.LEFT, expand=True)
        entry.pack(side=tk.LEFT, expand=True)

        # set button
        rateButton = tk.Button(self, width=20, height=2, text="Set", fg="red", command=lambda: setBtnClick(port, entry))
        rateButton.pack(side=tk.RIGHT, expand=True)
        
        # bpm button
        #bpmButton = tk.Button(self, width=20, height=2, text="BPM", fg="red", command=bpmBtnClick)
        #bpmButton.pack(anchor="s",side=tk.TOP, expand=True)

        #rate = tk.Label(self, text="?? bpm", fg="red")
        #rate.pack(anchor="s",side=tk.TOP, expand=True)


        dataButton = tk.Button(self, width=20, text="Collect Data >>", fg="red", command=lambda:[controller.show_frame(DataPage), dataBtnClick(port)])
        dataButton.pack(anchor="s", side=tk.TOP, expand=True)
       
        tk.Frame.pack(self,fill=tk.BOTH, side=tk.TOP, expand=True)

class DataPage(tk.Frame):
    
    def __init__(self, parent, controller):
        self.x_vals = []
        self.y_vals = []
        self.index = count()
        self.f = Figure(figsize=(6,5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.plot([1,2,3], [1,2,3])
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ECG Signal")
        label.pack(pady=10, padx=10)
        
        backBtn = tk.Button(self, text="Back to Home", 
                            command=lambda: controller.show_frame(StartPage, DataPage))
        backBtn.pack()
        
        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ani = None
        self.running = False
                
    def readECG(self): 
        value = port.read()
        print(f"Received {value}")
        if value:
            x = next(self.index)
            y = int(value)
            return x, y 
        else:
            return 0, 0
        
    def animate(self, frame):
        x, y = self.readECG()
        self.x_vals.append(x)
        self.y_vals.append(y)
        self.x_vals = self.x_vals[-50:]
        self.y_vals = self.y_vals[-50:]
        self.a.clear()
        self.a.plot(self.x_vals, self.y_vals)
        self.a.set_title("ECG Signal")
    
    def start(self):
        self.ani = animation.FuncAnimation(self.f, self.animate, interval=1, repeat=False)
        self.running = True
        self.ani._start()
        print("Started Animation..")
    
    def stop(self):
        self.running = False
        self.ani._stop()
        self.ani = None
        self.index = count()
        self.x_vals = []
        self.y_vals = []
        print("Stopped animation..")

        
app = Heart()
app.mainloop()