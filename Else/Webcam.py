import cv2
import time
import datetime

cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

#Lägg till egen path!!!

path="C:/Users/gabri/Videos/Webcamtest"
#path="C:/Users/Joakim/Documents/3an/Kandidatarbete/Egen programmering/Webcamtest"

frame_size = (int(cap1.get(3)), int(cap2.get(4)))
frame_size = (int(cap1.get(3)), int(cap2.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")
out1 = cv2.VideoWriter(path+"/"+current_time+"+v1"+".mp4", fourcc, 120, frame_size)
out2 = cv2.VideoWriter(path+"/"+current_time+"+v2"+".mp4", fourcc, 240, frame_size)

while True: 
        _, frame1 = cap1.read()
        _, frame2 = cap2.read()

        out1.write(frame1)
        out2.write(frame2)

        cv2.imshow("Camera1", frame1)
        cv2.imshow("Camera2", frame2)

        if cv2.waitKey(1) == ord('q'):
             break
        
        
out1.release()   
out2.release()    
cap1.release()
cap2.release()
cv2.destroyAllWindows()


        

        