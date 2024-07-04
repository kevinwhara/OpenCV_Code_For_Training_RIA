import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 720)

detector = HandDetector(maxHands=2,  detectionCon=0.8, minTrackCon=0.5)
startDist = None
scale = 0
cx, cv = 500,500

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True, flipType=True)
    img1 = cv2.imread("Zooming.png")

    if len(hands) == 2:
        if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and \
                detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:

            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]

            tipOfFirstFinger = lmList1[8][:2]
            tipOfSecondFinger = lmList2[8][:2]

            if startDist is None:
                # length, info, img = detector.findDistance(tipOfFirstFinger, tipOfSecondFinger, img)
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
                print(length)
                startDist = length

            # length, info, img = detector.findDistance(tipOfFirstFinger, tipOfSecondFinger, img)
            length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
            scale = int((length - startDist) // 2)
            cx, cv = info[4:]
            print(scale)

    else:
        startDist = None

    try:
        h1, w1, _ = img1.shape
        newH, newW = ((h1+scale)//2)*2, ((w1+scale)//2)*2 # sebelum dirubah h1+scale, w1+scale
        img1 = cv2.resize(img1, (newW, newH))

        img[cv-newH//2:cv+ newH//2, cx-newW//2:cx+ newW//2] = img1
    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)