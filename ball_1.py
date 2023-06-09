from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import requests
H_MIN = 0
H_MAX = 255
S_MIN = 0
S_MAX = 255
V_MIN = 0
V_MAX = 255


#default capture width and height
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
#max number of objects to be detected in frame
MAX_NUM_OBJECTS=50
#minimum and maximum object area
MIN_OBJECT_AREA = 20*20
MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH/1.5
font = cv2.FONT_HERSHEY_SIMPLEX
  
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())
url = "http://192.168.4.1"

#COMANDOS DO ROBO
commands = {
    "F": "State=F",
    "B": "State=B",
    "L": "State=L",
    "R": "State=R",
    "I": "State=I",
    "G": "State=G",
    "J": "State=J",
    "H": "State=H",
    "W": "State=W",
    "w": "State=w",
    "0": "State=0",
    "1": "State=1",
    "2": "State=2",
    "3": "State=3",
    "4": "State=4",
    "5": "State=5",
    "6": "State=6",
    "7": "State=7",
    "8": "State=8",
    "9": "State=9",
    "S": "State=S"
}

# PARA MANDAR COMANDOS
def send_command(command):
    try:
        r = requests.get(url, params=commands[command])
        if r.status_code == 200:
            print("Command sent successfully")
        else:
            print("Failed to send command")
    except:
        print("Failed to connect to server")

#CODIGO OPENCV






greenLower = (0, 208, 186)
greenUpper = (47, 255, 255)
pts = deque(maxlen=args["buffer"])
def quadrade_1(x1,y1):
	if x1 < 300 and y < 200:
		print("quadrante 1")
		send_command("F")
    

def quadrade_2(x2,y2):
	if x2 > 300 and y < 200:
		print("quadrante 2")
		send_command("L")
        send_command("F")
		send_command("9")
    

def quadrade_3(x3,y3):
	if x3 < 300 and y > 200:
		print("quadrante 3")
		send_command("B")

def quadrade_4(x4,y4):
	if x4 > 300 and y > 200:
		print("quadrante 4")
		print
		


if not args.get("video", False):
	vs = VideoStream(src=0).start()

else:
	vs = cv2.VideoCapture(args["video"])

time.sleep(2.0)

while True:
	
	frame = vs.read()
	
	frame = frame[1] if args.get("video", False) else frame
	
	
	if frame is None:
		break
	
	
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	
	
	
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	
	if len(cnts) > 0:
		
		
		
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		print(x,y)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		send_command("S")
		if radius > 10:
			x = int(x)
			y = int(y)
			cx = x
			cy = y
			quadrade_1(cx,cy)
			quadrade_2(cx,cy)
			quadrade_3(cx,cy)
			quadrade_4(cx,cy)
			cv2.circle(frame,(x,y),20,(0,255,0),2);
			if(y-25>0):
				cv2.line(frame,(x,y),(x,y-25),\
						(0,255,0),2)
			else:
				cv2.line(frame,(x,y),(x,0)\
						,(0,255,0),2)
			if(y+25<FRAME_HEIGHT):
				cv2.line(frame,(x,y),(x,y+25),\
						(0,255,0),2)
			else:
				cv2.line(frame,(x,y),(x,FRAME_HEIGHT),\
						(0,255,0),2)
			if(x-25>0):
				cv2.line(frame,(x,y),(x-25,y),\
						(0,255,0),2)
			else:
				cv2.line(frame,(x,y),(0,y),\
						(0,255,0),2)
			if(x+25<FRAME_WIDTH):
				cv2.line(frame,(x,y),(x+25,y),\
						(0,255,0),2)
			else:
				cv2.line(frame,(x,y),(FRAME_WIDTH,y),\
						(0,255,0),2)

			cv2.putText(frame,str(x)+","+str(y),\
						(x,y+30),1,1,(0,255,0),2)


	pts.appendleft(center)
      
                    
	
	for i in range(1, len(pts)):
		
		
		if pts[i - 1] is None or pts[i] is None:
			continue
		
		
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		break

if not args.get("video", False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()
