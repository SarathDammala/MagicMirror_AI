# Import OpenCV2 for image processing
import cv2
import picamera
import picamera.array
# Import numpy for matrices calculations
import numpy as np
import os;
import time;

userMap={};

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize and start the video frame capture
camera = picamera.PiCamera();
stream =  picamera.array.PiRGBArray(camera);
camera.resolution = (320, 240);
    
def readUserRegister():
    registerFile = os.getcwd() + "/setup/register.txt";
    registerReadFile = open(registerFile, "r");
    for line in registerReadFile:
       iD,Name = line.split("-");
       userMap[int(iD)] = str(Name[:-1]);

def recognizeFace():
    
    # Create Local Binary Patterns Histograms for face recognization
    recognizer = cv2.face.LBPHFaceRecognizer_create();

    # Load the trained mode
    recognizer.read('trainer/trainer.yml')

    # Load prebuilt model for Frontal Face
    cascadePath = "haarcascade_frontalface_default.xml"
    
    # Create classifier from prebuilt model
    faceCascade = cv2.CascadeClassifier(cascadePath);
    # Loop
    while True:
        # Read the video frame
        camera.capture(stream, 'bgr', use_video_port=True);
        stream.truncate(0);
        # Convert the captured frame into grayscale
        gray = cv2.cvtColor(stream.array,cv2.COLOR_BGR2GRAY)

        # Get all face from the video frame
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
            );

        # For each face in faces
        for(x,y,w,h) in faces:

            # Create rectangle around the face
            cv2.rectangle(stream.array, (x,y), (x+w, y+h), (255,0,0), 2)
           
            # Recognize the face belongs to which ID
            Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            try:
                Id = userMap[int(Id)];
                return str(Id);
            except:
                Id = "Unknown";
            
            # Put text describe who is in the picture
            cv2.rectangle(stream.array, (x,y), (x+w, y+h), (255,0,0), 2)
            cv2.putText(stream.array, str(Id), (x,y-40), font, 1, (255,255,255), 1)

        # Display the video frame with the bounded rectangle
        cv2.imshow('image',stream.array) 

        # If 'q' is pressed, close program
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break;
    return "Unknown";
        

def findUser():

    readUserRegister();
    userName = recognizeFace();
# Close all windows
    cv2.destroyAllWindows();
    return userName;
