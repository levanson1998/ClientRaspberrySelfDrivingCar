from time import sleep
from client import SocketProcess
# from transmit_serial import SerialProcess
ReStop=1
SpeedCurrent=20
isTracking = 1
PiStop=0
a=10.1
i=0

# stop? = (btnStop, raspStop)
# start? = (btbStart, raspStart)
while True:
    a+=0.000001
    isStart, sttSpeed = SocketProcess(isTracking, ReStop, SpeedCurrent)
    # print("{} == {}".format(isStart, sttSpeed))
    # if(PiStop==1):
    #     isStart=0 # (stop)

    # z = np.polyfit(cx, cy, 3)
    # a = np.polyval(z, x)
    # SpeedCurrent, ReStop =SerialProcess(a, isStart, sttSpeed)
    i = (i+1)%3
    print("i: ", i)
    isTracking=i-1
    sleep(10)
