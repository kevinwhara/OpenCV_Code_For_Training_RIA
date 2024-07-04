import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 720)

def nothing(x):
    pass

cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

# Define colors and their initial HSV ranges
colors = [
    {"name": "blue", "lower": [92, 57, 50], "upper": [142, 153, 178]},
    {"name": "green", "lower": [40, 40, 40], "upper": [80, 255, 255]},
    {"name": "red", "lower": [0, 100, 100], "upper": [10, 255, 255]}
]

# Create trackbars for each color
for color in colors:
    cv2.createTrackbar(f'Lower_H_{color["name"]}', 'live transmission', color["lower"][0], 255, nothing)
    cv2.createTrackbar(f'Lower_S_{color["name"]}', 'live transmission', color["lower"][1], 255, nothing)
    cv2.createTrackbar(f'Lower_V_{color["name"]}', 'live transmission', color["lower"][2], 255, nothing)
    cv2.createTrackbar(f'Upper_H_{color["name"]}', 'live transmission', color["upper"][0], 255, nothing)
    cv2.createTrackbar(f'Upper_S_{color["name"]}', 'live transmission', color["upper"][1], 255, nothing)
    cv2.createTrackbar(f'Upper_V_{color["name"]}', 'live transmission', color["upper"][2], 255, nothing)

while True:

    success, img = cap.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Iterate through colors and get current trackbar positions
    for color in colors:
        l_h = cv2.getTrackbarPos(f'Lower_H_{color["name"]}', 'live transmission')
        l_s = cv2.getTrackbarPos(f'Lower_S_{color["name"]}', 'live transmission')
        l_v = cv2.getTrackbarPos(f'Lower_V_{color["name"]}', 'live transmission')
        u_h = cv2.getTrackbarPos(f'Upper_H_{color["name"]}', 'live transmission')
        u_s = cv2.getTrackbarPos(f'Upper_S_{color["name"]}', 'live transmission')
        u_v = cv2.getTrackbarPos(f'Upper_V_{color["name"]}', 'live transmission')

        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, l_b, u_b)

        cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            area = cv2.contourArea(c)
            if area > 2000:
                cv2.drawContours(img, [c], -1, (255, 0, 0), 3)
                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(img, (cx, cy), 7, (255, 255, 255), -1)
                cv2.putText(img, f'{color["name"]} Detected', (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        res = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("live transmission", img)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()