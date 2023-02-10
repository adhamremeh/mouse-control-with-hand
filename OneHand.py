import cv2
import mediapipe as mp
import time
import mouse
from pynput.mouse import Button, Controller
import pyautogui
import sys

cap = cv2.VideoCapture(0)

print("The Applications Started Succefully Try make Some Gestsures")
print("1- Center Your Hand Rotation To Activate The Gestures")
print("2- Bend your index to move the cursor")
print("3- Bend your pinky hardly to click the mouse")
print("4- Bend your ring finger hardly to right click the mouse")
print("5- Bend your middle finger hardly to double click the mouse")


mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

cx = 0
cx1 = 0
cx3 = 0
cx6 = 0
cx8 = 0
cx12 = 0
cx16 = 0
cx20 = 0
cy = 0
cy1 = 0
cy3 = 0
cy6 = 0
cy8 = 0
cy12 = 0
cy16 = 0
cy20 = 0
diffMove = 0
diffClick = 0
diffRightClick = 0
diffDouble = 0
diffOn = 0

handIndex = 0

Release = False

def map(i, max, maxOut):
    return int((maxOut/max)*(i))

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        if (len(results.multi_hand_landmarks) > 1):
            handIndex = 1
        else:
            handIndex = 0
        mpDraw.draw_landmarks(img,  results.multi_hand_landmarks[handIndex], mpHands.HAND_CONNECTIONS)
        for id, lm in enumerate(results.multi_hand_landmarks[handIndex].landmark):
            h, w, c = img.shape
            if id == 9:
                cx, cy = int(lm.x *w), int(lm.y*h)
                cx = 1980 - map(cx, 550, 1980)
                cy = map(cy, 250, 1080)
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
            if id == 1:
                cx1, cy1 = int(lm.x *w), int(lm.y*h)
                cv2.circle(img, (cx1,cy1), 3, (255,0,255), cv2.FILLED)
            if id == 3:
                cx3, cy3 = int(lm.x*w), int(lm.y*h)
                cv2.circle(img, (cx3,cy3), 3, (255,0,255), cv2.FILLED)
            if id == 6:
                cx6, cy6 = int(lm.x *w), int(lm.y*h)
                cv2.circle(img, (cx6,cy6), 3, (255,0,255), cv2.FILLED)
            if id == 8:
                cx8, cy8 = int(lm.x *w), int(lm.y*h)
                cv2.circle(img, (cx8,cy8), 3, (255,0,255), cv2.FILLED)
            if id == 12:
                cx12, cy12 = int(lm.x *w), int(lm.y*h)
                cv2.circle(img, (cx12,cy12), 3, (255,0,255), cv2.FILLED)
            if id == 16:
                cx16, cy16 = int(lm.x *w), int(lm.y*h)
                cv2.circle(img, (cx16,cy16), 3, (255,0,255), cv2.FILLED)
            if id == 20:
                cx20, cy20 = int(lm.x *w), int(lm.y*h)
                cv2.circle(img, (cx20,cy20), 3, (255,0,255), cv2.FILLED)

            diffMove = cy8 - cy6
            diffClick = cy20 - cy3
            diffRightClick = cy16 - cy3
            diffDouble = cy12 - cy3
            diffOn = cx12 - cx1
            if diffMove < 0:
                diffMove *= -1
            if diffClick < 0:
                diffClick *= -1
            if diffRightClick < 0:
                diffRightClick *= -1
            if diffDouble < 0:
                diffDouble *= -1
            if diffOn < 0:
                diffOn *= -1

            #print("Move:", diffMove)            
            #print("Click:", diffClick)
            #print("Right Click:", diffRightClick)
            #print("Double:", diffDouble)
            #print("On:", diffOn)

            if diffOn < 45 and diffOn > 0 and cy12 < cy1 :
                if diffMove < 15 and diffMove > 0:
                    mouse.move(cx+210, cy-140)
                if diffDouble < 10 and diffDouble > 0:
                    if Release == False:
                        Controller().click(Button.left, 2)
                        Release = True
                elif diffClick < 15 and diffClick > 0:
                    if Release == False:
                        Controller().click(Button.left)
                        Release = True
                elif diffRightClick < 15 and diffRightClick > 0:
                    if Release == False:
                        Controller().click(Button.right)
                        Release = True
                else:
                    if Release == True:
                        Controller().release(Button.left)
                        Release = False

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)