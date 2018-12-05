from camera.object_detector import CAMERA_ORIGIN
import numpy as np
import cv2

stream = cv2.VideoCapture(1)

if __name__ == '__main__':
    while(True):
        # Capture frame-by-frame
        ret, frame = stream.read()

        # Our operations on the frame come here
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.circle(frame, CAMERA_ORIGIN, 5, (255, 0, 0))
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    stream.release()
    cv2.destroyAllWindows()
