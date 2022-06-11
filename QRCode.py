import numpy as np
from pyzbar.pyzbar import decode
from datetime import datetime
import cv2 as cv

class QRCodeClass():
    def __init__(self,vid):
        self.vid = vid
        self.vid.set(3,640)
        self.vid.set(4,720)
        


    def decode_vid(self):
       while True:
            ret,img = self.vid.read()
            for barcode in decode(img):
                    text = barcode.data.decode('utf-8')
                    authorized_text = text[0:10]
                    if text[0:10] == 'Authorized':
                        color = (0,255,0)
                        text = authorized_text
                    else:
                        text = 'Non-Authorized'
                        if ret:
                            # if video is still left continue creating images
                            name = f'suspicious_entry_{datetime.date(datetime.now())}' + '.jpg'
                            print('Creating...' + name)

                            # writing the extracted images
                            cv.imwrite(name, img)
                            break_flag = True



                    polygon_points = np.array([barcode.polygon], np.int32)
                    polygon_points=polygon_points.reshape(-1,1,2)
                    rect_points= barcode.rect
                    cv.polylines(img,[polygon_points],True,color, 3)
                    cv.putText(img, text, (rect_points[0],rect_points[1]), cv.FONT_HERSHEY_DUPLEX, 0.8,color, 2)
            cv.imshow("Video", img)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break