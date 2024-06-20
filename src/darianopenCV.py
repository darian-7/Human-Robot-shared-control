#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 07 21:44:01 2022

@author: darian
"""

import sys
import cv2

cascadePath = sys.argv[1]   # Collects values supplied by me.
Cascadeface = cv2.CascadeClassifier(cascadePath)    # Loads face cascade into memory so that it's ready to use.

webcamdata = cv2.Videocapture(0)   # Sets video source for facial recognition to in-built webcam which OpenCV uses.

while True:
    
    videoframe = webcamdata.read()  # Read function captures video from the webcam frame by frame.
    
    grayscale = cv2.cvtColor(videoframe, cv2.COLOR_BGR2GRAY)    # Converts images gathered from webcam into grayscale because many operations in OpenCV are done in grayscale.
    
    myface = Cascadeface.detectMultiscale(  # detectMultiscale function detects objects on the face cascade.
        gray,   # Image type: grayscale.
        ScaleFactor=1.2
        minNeighbors=5,     # Determines how many objects are detected near the selected one before a face is detected.
        minSize=(35,35),     # Determines the size of each window.
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE      # This function returns a list of rectangles when it thinks a face is detected.
    )
    
    for (x, y, w, h) in faces:
        cv2.rectangle(videoframe, (x, y), (x+w, y+h), (0, 225, 0), 2)   # Places a rectangle around a detected face.
    
    cv2.imshow('Video', videoframe)     # Displays the frame as a result of code above^.
    
    if cv2.waitKey(1) & 0xFF == ord('s'):   # If the 's' key is pressed the script is stopped and exited.
        break
    
webcamdata.release()
cv2.destroyAllWindows()     # When everything is over, the capture is released.










# Tiwari, Shantnu Face Recognition with Python, in Under 25 Lines of Code [source code]. https://realpython.com/face-recognition-with-python/