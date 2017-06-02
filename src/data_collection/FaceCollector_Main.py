import cv2, sys, os, time, logging

video = cv2.VideoCapture(0)

while True:
    ret, cameraFrame = video.read()
    if not ret:
        exit()
    cv2.imshow("Live Video", cameraFrame)
    if cv2.waitKey(1) == ord('q'):
        break
    continue