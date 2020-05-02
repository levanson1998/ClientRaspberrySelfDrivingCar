import serial
import time
from threading import Thread, Timer
import os
import sys
import numpy as np


a=1

isTracking=1
# =1: start, =0: stop
isStart=1
# =1: fast, =0: slow
SttSpeed=1
# receive from stm
speedCurrent=10

time_t=0.1
t=0

ser = serial.Serial(
    port = 'COM8',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

next_call = time.time()
# start, stop, fast, slow, 
# 
def send_serial():
    global a, isStart, SttSpeed, next_call, time_t, t, speedCurrent
    # 100.123 => 100 & 1230
    # 123.34556365
    # 123.3456
    # a1 = 123
    # a2 = 3456
    # a2 = 1230.0

    a1 = int(a)
    a2 = int(round((a-a1)*10000))
    
    dataa1=a1.to_bytes(2, byteorder = "little", signed = True)
    a1L=dataa1[1]
    a1H=dataa1[0]
    dataa2=a2.to_bytes(2, byteorder = "little", signed = True)
    a2L=dataa2[1]
    a2H=dataa2[0]

    packet = [a1L, a1H, a2L, a2H, isStart,SttSpeed]
    # print(packet)
    print("{} * {} * {} * {} * {}".format(a, a1, a2, isStart,SttSpeed))
    #print("time: ",time.time())
    # packet = [chr(dataIsTracking), chr(dataX1), chr(dataX2), chr(dataY1), chr(dataY2)]
    # print("{} - - {}".format(packet, type(packet)))

    ser.write(packet)

    receiveData = ser.read(2)
    if(len(receiveData)!= 0):
        speedCurrent=receiveData[0]+receiveData[1]/100
    t+=1
    
    next_call = next_call + time_t
    Timer( next_call - time.time(), send_serial ).start()

send_serial()

# from (Pi, android, android)
def SerialProcess(aIn, isStartIn, SttSpeedIn):
    global a, isStart, SttSpeed, speedCurrent
    a = aIn
    isStart=isStartIn
    SttSpeed=SttSpeedIn
    return speedCurrent



