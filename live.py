# -*- coding: utf-8 -*-
"""
Created on Sat May  9 02:52:09 2020

@author: Dell
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()   
plt.ion()
plt.show()

def f(x, y):
    return np.sin(x) + np.cos(y)

#def updatefig(*args):
#    global x, y

x_vals = []
y_vals = []
im = plt.imshow()

x = np.linspace(0, 2 * np.pi, 120)
y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)
im = plt.imshow(f(x, y))    

#for i in range(500):

#    x += np.pi / 15.
#    y += np.pi / 20.
#    im.set_array(f(x, y))
#    plt.draw()
#    plt.pause(0.0000001)