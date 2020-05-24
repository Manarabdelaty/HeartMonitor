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

# Documentation

The emebedded application is implemented using Round Robin with Interrupts archietecure.

The application is composed of three main interrupts with the following callback functions: 

1) UART Receive Interrupt `HAL_UART_RxCpltCallback`

This callback function is called whenever a UART receive interrupt is generated. The uart interrupt is generated whenever it receives 16-bytes.

2) ADC Conversion Complete Interrupt `HAL_ADC_ConvCpltCallback`

This callback function is called whenver the ADC succesfuly completes the conversion of one ADC sample.

3) Timer Period Elapsed Interrupt `HAL_TIM_PeriodElapsedCallback`

This callback function is called whenver TIM2 period has elapsed (whenever one minute has passed).

