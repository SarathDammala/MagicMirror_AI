import cv2
import picamera
import picamera.array
import sys;
import training;
import random;

def createDataSet(iD):
# Set Camera defaults
    camera = picamera.PiCamera();
    stream =  picamera.array.PiRGBArray(camera);
    camera.resolution = (320, 240);
# Detect object in video stream using Haarcascade Frontal Face
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
# For each person, one face id
    face_id = iD;
# Initialize sample face image
    count = 0;

    while True:
# Use Pi Camera to get the feed.        
        camera.capture(stream, 'bgr', use_video_port=True);
# stream.array now contains the image data in BGR order
        gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
# Debug windows to show what Camera is seeing.        
        cv2.imshow('frame_color', stream.array);
        cv2.imshow('frame_gray', gray);

# Use the above cascade to detect frontal faces. 
        faces = faceCascade.detectMultiScale(
             gray,     
             scaleFactor=1.2,
             minNeighbors=5,     
             minSize=(20, 20)
            );
# Find the face in the stream and mark it and save it.

        for (x,y,w,h) in faces:
            count += 1;
            cv2.rectangle(stream.array,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = stream.array[y:y+h, x:x+w]
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('frame_face', stream.array);

# After 100 samples quit the process or when user presses "q".
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif count>100:
            break
        # reset the stream before the next capture
        stream.seek(0)
        stream.truncate()

def registerUser(iD, userName):
    print iD;
    print userName;
    registerFile = open("setup/register.txt","a");
    registerFile.write (str(iD) + "-" + str(userName) + '\n');
    createDataSet(iD);

name = sys.argv[1];
iD = int(random.randint(1,100)*3.14);
registerUser(iD,name);
training.trainForNewUser();

