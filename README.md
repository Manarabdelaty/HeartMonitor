# HeartSensor

# Hardware

The application utlizies the following hardware components:

1) STM32 Blue pill as the microcontroller
2) AD8238 Heart monitor sensor
3) USB-UART Bridge from SCI-Lab

# Dependecies

- ARM C/C++ compiler
- Python 3.7
- pyserial 3.4
- matplotlib 3.2.1
- tkinter

The emebedded application is developed using ARM Keil MDK and CubeMX toolchains.
The PC application is developed using Python. 

# Usage

To run the python application, invoke the following from the terminal

```
python tkApp.py 
```

To run/flash the embedded application, you can use microvision Keil IDE. 
