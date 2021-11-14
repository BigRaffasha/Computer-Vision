import cv2, math
import mediapipe as mp

class handdetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.8, trackingCon = 0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackingCon)
        self.tipIds = [4, 8, 12, 16, 20]

    # Find Hands
    def findhands(self, image, draw = True):
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image)

        # Draw the hand annotations on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())

        return image

    # Print hand ID and position
    def handposition(self, image, handNum=0, draw=True):
        xList = []
        yList = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])

        return self.lmList

    # Check which fingers are up
    def fingersUp(self):
        fingers = []

        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    
            # Fingers
        for id in range(1, 5):
    
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                continue

        return fingers


    # Find distance between 2 points
    def findDistance(self, p1, p2, img, draw=True,r=5, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
 
        return length, img, [x1, y1, x2, y2, cx, cy]

def main():
    # For webcam input:
    cap = cv2.VideoCapture(0)
    detector = handdetector()

    while True:
        success, image = cap.read()
        findhands = detector.findhands(image)
        handposition = detector.handposition(image)

        # Flip the image horizontally for a selfie_view display and Display the Camera
        cv2.imshow('Camera', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

if __name__ == "__main__":
    main()