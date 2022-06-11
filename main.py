import cv2
import numpy as np
import face_recognition 
import os
from pyzbar.pyzbar import decode 
from datetime import  datetime
from db import Database 

db = Database('records.db')

def resize(img, size) :
    width = int(img.shape[1]*size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation= cv2.INTER_AREA)

path = 'personnel_images'
studentImg = []
studentName = []
myList = os.listdir(path)
for cl in myList :
    curimg = cv2.imread(f'{path}/{cl}')
    studentImg.append(curimg)
    studentName.append(os.path.splitext(cl)[0])

def findEncoding(images) :
    imgEncodings = []
    for img in images :
        img = resize(img, 0.50)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeimg = face_recognition.face_encodings(img)[0]
        imgEncodings.append(encodeimg)
    return imgEncodings



def markAttendance(name):
        nameList = []
        tuple = []        
        for index, tuple in enumerate(db.fetchAttendance()):
            nameList.append(tuple[1])
        
        if tuple == []:
            attendanceDate = datetime.now()
            db.insertAttendance(name,attendanceDate)
        elif name not in nameList:
            attendanceDate = datetime.now()
            db.insertAttendance(name,attendanceDate)

EncodeList = findEncoding(studentImg)

vid = cv2.VideoCapture(0)
while True :
    success, frame = vid.read()
    frame = cv2.flip(frame , 1)
    Smaller_frames = cv2.resize(frame, (0,0), None, 0.25, 0.25)

    facesInFrame = face_recognition.face_locations(Smaller_frames)
    encodeFacesInFrame = face_recognition.face_encodings(Smaller_frames, facesInFrame)

    for encodeFace, faceloc in zip(encodeFacesInFrame, facesInFrame) :
        matches = face_recognition.compare_faces(EncodeList, encodeFace, tolerance=0.5)
        facedis = face_recognition.face_distance(EncodeList, encodeFace)
        # print(facedis)
        matchIndex = np.argmin(facedis)

        if matches[matchIndex] :
            name = studentName[matchIndex].upper()
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.rectangle(frame, (x1, y2-25), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
    
    # QR CODE
    for barcode in decode(frame):
        text = barcode.data.decode('utf-8')
        authorized_text = text[0:10]
        if text[0:10] == 'Authorized':
            color = (0,255,0)
            text = authorized_text
        else:
            text = 'Non-Authorized'
            if success:
                # if video is still left continue creating images
                name = f'suspicious_entry_{datetime.date(datetime.now())}' + '.jpg'
                print('Creating...' + name)

                # writing the extracted images
                cv2.imwrite(name, frame)
                break_flag = True



        polygon_points = np.array([barcode.polygon], np.int32)
        polygon_points=polygon_points.reshape(-1,1,2)
        rect_points= barcode.rect
        cv2.polylines(frame,[polygon_points],True,color, 3)
        cv2.putText(frame, text, (rect_points[0],rect_points[1]), cv2.FONT_HERSHEY_DUPLEX, 0.8,color, 2)

    cv2.imshow('video',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
                break