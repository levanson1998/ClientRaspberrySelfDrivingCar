from time import sleep
from client import SocketProcess
from transmit_serial import SerialProcess


SpeedCurrent=20
isTracking = 1
PiStop=0
a=10.1

# stop? = (btnStop, raspStop)
# start? = (btbStart, raspStart)
while True:
    a+=0.000001
    isStart, sttSpeed = SocketProcess(isTracking, SpeedCurrent)
    # print("{} == {}".format(isStart, sttSpeed))
    # if(PiStop==1):
    #     isStart=0 # (stop)

    # z = np.polyfit(cx, cy, 3)
    # a = np.polyval(z, 3)
    SpeedCurrent=SerialProcess(a, isStart, sttSpeed)
