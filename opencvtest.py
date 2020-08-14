import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if(cap.isOpened() == False):
	print("Error opening video stream")
	exit(0)

cap.set(3,1600)
cap.set(4,900)

while(cap.isOpened()):
	ret, frame = cap.read()

	if(ret == True):
		cv2.imshow('Frame',frame)

		if(cv2.waitKey(25) & 0xFF == ord('q')):
			break;
	else:
		break;

cap.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
for a in range (1,5):
	cv2.waitKey(1)