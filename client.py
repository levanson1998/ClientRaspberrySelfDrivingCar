import socketio
from time import sleep
import datetime
import base64
from threading import Thread

isTracking=0
timerLost=2.0
url_heroku = "https://seft-drivingcar.herokuapp.com/"
# url_heroku = "http://localhost:3000/"
status = "Run"
speed = 1.0

isStart=0
sttSpeed=0

sio = socketio.Client()
sio.connect(url_heroku)
print('my sid is: ', sio.sid)

@sio.on('connect')
def on_connect():
	print("I'm connected!\n")
	sio.emit('car-on',True)		

@sio.on('car-send-stt-ok')
def on_message(data):
	print('Server has received your status\n')

@sio.on('car-send-img-ok')
def on_message1(data):
	print('Server has received your image\n')

@sio.on('from-server')
def sioSendPicTime(data):
	global isStart, sttSpeed
	case = data
	if (case=="start"):
		isStart=1
	elif (case=="stop"):
		isStart=0
	elif (case=="fast"):
		sttSpeed=1
	elif (case=="slow"):
		sttSpeed=0
	elif (case=="getpic"):
		pic = capturePic()
		capturedTime = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
		mydict_img = {"Image": "data:image/jpg;base64," + pic.decode("utf-8"), "CapTime":capturedTime}
		sio.emit('car-send-img', mydict_img)

	print("android -> {}".format(case))
	# request ok
	sio.emit("from-server-ok", case)

@sio.on('disconnect')
def on_disconnect():
	try:
		sio.connect(url_heroku)
	except:
		print("I'm disconnected !")


# chup hinh anh tu camera
def capturePic():
	with open("./image.jpg","rb") as file:
		jpg_as_text = base64.b64encode(file.read())
	return jpg_as_text

def sioSendStt():
	global status, speed
	while True:
		mydict = {"status":status,"speed":speed}
		sio.emit("car-send-stt", mydict)
		print("sioSendStt status: {}  speed: {}".format(status, speed))
		sleep(4)
# goi toc do
threadSendStt = Thread(target = sioSendStt)
threadSendStt.start()

# main of client.py
def SocketProcess(isTracking, speed1):
	# status (rasp ---> android)
	# speed (stm ---> serial ---> client ---> android)
	# btnStart/Stop & Fast/Slow (android ---> client ---> stm)
	global status, isStart, sttSpeed, speed
	speed=speed1
	if (isTracking==1):
		status = "Run"
	elif (isTracking==0):
		status = "Stop"
	elif (isTracking==-1):
		status = "Lost"
	
	# btnStart/Stop & Fast/Slow => serial
	return isStart, sttSpeed
