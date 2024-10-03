import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

# Open up webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Setting hand detector
detector = HandDetector(maxHands=1)

# Setting Timer
timer = 0
stateResult = False
startGame = False
scores = [0,0]

while True:
    imgBG = cv2.imread("Resources/BG.png")
    
    # Gives image and success boolean
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find hands
    hands, img = detector.findHands(imgScaled) # with draw

    # Starting Game
    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            # Setting up timer in picture
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    # Main hand
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    # Setting up players rock, paper, scissor
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3

                    randomNumber = random.randint(1,3)
                    imgAi = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    ingMB = cvzone.overlayPNG(imgBG, imgAi, (149, 310))

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # Ai Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

                    
    # Putting the scaled Webcam onto the background
    imgBG[234:654,795:1195] = imgScaled

    if stateResult:
        ingMB = cvzone.overlayPNG(imgBG, imgAi, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled", imgScaled)


    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
        
    