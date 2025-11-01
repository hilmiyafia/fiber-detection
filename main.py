
import cv2
import numpy as np

video = cv2.VideoCapture("video.mp4")
FONT = cv2.FONT_HERSHEY_PLAIN
RECT = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
BLUE = (255, 0, 0)
CYAN = (255, 255, 0)
CALLIBRATION = 14022

while True:
    retval, image = video.read()
    if not retval: break
    gray = image[:, :, 0]
    _, binary = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    output = cv2.connectedComponentsWithStats(binary, 4, cv2.CV_32S)
    num, labels, stats, centroids = output
    for i in range(1, num):
        x1 = stats[i, cv2.CC_STAT_LEFT]
        y1 = stats[i, cv2.CC_STAT_TOP]
        x2 = x1 + stats[i, cv2.CC_STAT_WIDTH]
        y2 = y1 + stats[i, cv2.CC_STAT_HEIGHT]
        a = stats[i, cv2.CC_STAT_AREA]
        p = np.zeros_like(binary)
        p[labels == i] = 255
        p = np.sum(p - cv2.morphologyEx(p, cv2.MORPH_ERODE, RECT))
        d = p * (p / 16) - a
        if d < 0: continue
        l = (p / 4 + d ** 0.5) / CALLIBRATION
        w = (a / l) / CALLIBRATION
        if l < 1: continue
        text = f"Length: {l:.2f} cm"
        image = cv2.rectangle(image, (x1, y1), (x2, y2), BLUE, 4, 1)
        image = cv2.putText(image, text, (x1, y1), FONT, 1.5, CYAN, 2, 1)
    cv2.imshow("Video", image)
    cv2.waitKey(33)
cv2.waitKey()
video.release()
