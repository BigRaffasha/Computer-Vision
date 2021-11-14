import cv2, handmodule, pyautogui
import mediapipe as mp
import numpy as np

# Camera Resolution
wCam, hCam = 640, 480
wScr, hScr = pyautogui.size()

# Camera input
print(
    """
    0. Laptop Webcam
    1. External Camera
    """)
cam = input("Select active camera: ")
cap = cv2.VideoCapture(int(cam))
cap.set(3, wCam)
cap.set(4, hCam)
detector = handmodule.handdetector()

while cap.isOpened():
    success, image = cap.read()
    image = detector.findhands(image)
    lmList = detector.handposition(image)

    # Check which finger are up
    if len(lmList) != 0:
        xIndex, yIndex = lmList[8][1:]
        xMid, yMid = lmList[12][1:]

        fingers = detector.fingersUp()
        print(fingers)

        # Moving mode (Index finger up)
        if fingers[1]==1 and fingers[2]==0:
            # Draw Rectangle Border
            frame = 50
            cv2.rectangle(image, (frame, frame), (wCam-frame,hCam-frame), (0,0,255),)

            # Convert coordinates
            xMouse = np.interp(xIndex, (frame,wCam-frame), (0,wScr))
            yMouse = np.interp(yIndex, (frame,hCam-frame), (0,hScr))

        # Clicking mode (Index and middle finger up)
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
            lenght, image, filler = detector.findDistance(8, 12, image)

            if lenght<25:
                pyautogui.click()

        if fingers[0]==0 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:

            # Convert coordinates
            frame = 50
            xMouse = np.interp(xIndex, (frame,wCam-frame), (0,wScr))
            yMouse = np.interp(yIndex, (frame,hCam-frame), (0,hScr))

            pyautogui.dragTo(xMouse, yMouse, button='middle')

    # Display Window
    cv2.imshow("Camera", cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
        break
