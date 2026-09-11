import cv2 as cv
import sys
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import math

position = None
displacement = None
new_click = False


def mouse_call(event, x, y, flags, param):
    global position
    
    global new_click
    if event == cv.EVENT_LBUTTONDOWN:
     position = (x,y)
     new_click = True

     

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("could not acces camera")
    exit()

cv.namedWindow("Camera")
cv.setMouseCallback("Camera", mouse_call)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    height, width = frame.shape[0:2]

    roi = frame[80:251, 100:301]
    

    centre = (int(width/2), int(height/2))

    

    zeros = np.zeros(frame.shape[0:2], dtype=np.uint8)
      
    zeros[80:251, 100:301] = 255
      
    
    
    
    
    if new_click:
      print("Clicked at", position)
      displacement = (position[0] - centre[0], position[1] - centre[1])
      print("displacement from ref to chosen point is:", displacement[0],"to right and", displacement[1],"down")
      distance = math.hypot(displacement[0], displacement[1])
      print("distance is", distance)
      angle = math.atan2(displacement[1], displacement[0])
      dx = str(displacement[0])
      dy = str(displacement[1])
      d = str(round(distance,2))
      theta = str(round(math.degrees(angle),2))
      print(angle, "rad clockwise from x axis of reference point")

      
      
      new_click = False
    if position is not None:
         cv.circle(frame, position, 10, (0, 0, 255), -1)
         cv.line(frame, position, centre, (0,255,0), 5)
         cv.putText(frame, ("dx: " + dx + "px"), (520,30), cv.FONT_HERSHEY_COMPLEX, 0.6, (0,0,255), 1)
         cv.putText(frame, ("dy: " + dy + "px"), (520,60), cv.FONT_HERSHEY_COMPLEX, 0.6, (0,255,0), 1)
         cv.putText(frame, ("dist: " + d + "px"), (520,90), cv.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 1)
         cv.putText(frame, ("angle: " + theta), (520,120), cv.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 1)

     

    cv.imshow("Camera", frame)
    cv.imshow("Partial", roi)
    cv.imshow("mask", zeros)

    if cv.waitKey(1) == ord("q"):
     break

cap.release()
cv.destroyAllWindows()
print("final position", position)