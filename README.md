# HeartSensor

This is a heart monitor embedded application. The block diagram is shown below. 

![PPT](https://user-images.githubusercontent.com/25064257/82758441-df24ef00-9de6-11ea-93c3-1b6ef8e685f2.png)



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

The python application communicates with microcontroller over UART via three commands. 

1) `rate={new_rate};`  : this command sets a new sample rate for the STM32 internal ADC
2) `data;`             : this command starts the data collection for one minute
3) `hbpm;`             : this command computes the heart beats per minute. 

The emebedded application is implemented using Round Robin with Interrupts archietecure. The main loop continuously polls over the following three flags to check which command is received: 
- `set_sample_rate` : if raised, a new sample rate is set to the ADC. This done by computing a new value for TIM3 ARR register using the following equation: 
```
ARR = ((float) sysclk / (pre-scaler + 1) / (float)new_sample_rate) - 1;
``` 
The new timer period is set using `__HAL_TIM_SET_AUTORELOAD` function. 

- `collect_data`: if raised, the data collection is started; ADC starts conversion for one minute. This is done by starting TIM3 (sample rate timer) using `HAL_TIM_Base_Start` and TIM2 (one minute timer) using `HAL_TIM_Base_Start_IT` which starts the timer in the interrupt mode to generate an interuupt when TIM2 period elapses i.e when one minute passes. Inside the callback of TIM2 elapsed period, the two timers are stopped marking the end of the data collection. 

- `compute_bpm`: if raised, the ADC starts conversion for one minute. The generated digital signal is analyzed to count the peaks in the signal and according to the calculated number the beats per minute is reported. 

The application is composed of three main interrupts with the following callback functions: 

1) UART Receive Interrupt `HAL_UART_RxCpltCallback`

This callback function is called whenever a UART receive interrupt is generated. The uart interrupt is generated whenever it receives 16-bytes.

2) ADC Conversion Complete Interrupt `HAL_ADC_ConvCpltCallback`

This callback function is called whenver the ADC succesfuly completes the conversion of one ADC sample.

3) Timer Period Elapsed Interrupt `HAL_TIM_PeriodElapsedCallback`The emebedded application is developed using ARM Keil MDK and CubeMX toolchains. The PC application is developed using Python.

This callback function is called whenver TIM2 period has elapsed (whenever one minute has passed).

