import cv2
import os
#from tesseractPy import run_tesseract
import numpy as np
import sys
try:
    import Image
except ImportError:
    from PIL import Image
from pytesseract import run_tesseract

#--path to this file
filepath = os.path.dirname(__file__)
print filepath

#choose Camera
cap = cv2.VideoCapture(0)

#choose cascade for search
#cascPath = 'rus_plate_cascade.xml'
#cascPath = 'haarcascade_licence_plate_rus_16stages.xml'
cascPath = 'haarcascade_russian_plate_number.xml'

# Create the haar cascade 
Cascade = cv2.CascadeClassifier(cascPath)

#Blank picture
test = cv2.imread(filepath + '\BLANK.png')

while True:
    #get frame in cam
    ret,frame = cap.read()
    #get frame gray
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #Detect Object in the frame
    faces = Cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )

    #Draw a rectangle around the Object
    for (x,y,w,h) in faces:
        cropped = frame[(y*1.1):(y+(h*0.9)), (x*1.1):(x+(w*0.7))]
        
        cropped = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
        ret,cropped = cv2.threshold(cropped,120,255,cv2.THRESH_BINARY_INV)
        #save in new tes.png file
        cv2.imwrite('tes.png', cropped)
        #read this image with tesseract and write text in output.txt
        run_tesseract('tes.png','output', 'bla')
        
        #run_tesseract('tes.png', 'output')
        #open file with text on image and show it
        f=open('output.txt')
        print('Trying read number...')
        print f.read()
        f.close()
        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0) ,2)

    # Display the resulting frameq
    cv2.imshow('frame', frame)
    
    #try show Object, if found then save Object in the tes.png file
    try:
        cv2.imshow('face', cropped)      
    #else show message
    except NameError:
        cv2.imshow('face',test)

        
    #exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything done, release the capture    
cap.release()
cv2.destroyAllWindows()
