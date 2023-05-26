import os
import datetime
import cv2

cap  = cv2.VideoCapture(6)
assert cap.isOpened(), 'Cannot capture source'
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('img', frame)
        key = cv2.waitKey(1)
        
        if key & 0xFF == ord('q'):
            break

        if key & 0xFF == ord('s'):
            time = datetime.datetime.now()
  
            cv2.imwrite('./img/img-{}.jpg'.format(time.strftime("%Y-%m-%d-%H-%M-%S")), frame)
    else:
        print('can not get frame!')
        break