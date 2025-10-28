
import cv2
import numpy as np

video = cv2.VideoCapture("video.mp4")
FONT = cv2.FONT_HERSHEY_PLAIN
CIRCLE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
RECT = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
CALLIBRATION = 14022

while True:
    retval, frame = video.read()
    if not retval:
        cv2.imshow("Video", image)
        break
    image = cv2.resize(frame, (720, 480))
    gray = image[:, :, 0]
    _, binary = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, CIRCLE)
    output = cv2.connectedComponentsWithStats(cleaned, 4, cv2.CV_32S)
    num, labels, stats, centroids = output
    for i in range(1, num):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        a = stats[i, cv2.CC_STAT_AREA]
        p = np.zeros_like(cleaned)
        p[labels == i] = 255
        p = np.sum(p - cv2.morphologyEx(p, cv2.MORPH_ERODE, RECT))
        det = p * (p / 16) - a
        if det < 0: continue
        length = p / 4 + det ** 0.5
        width = a / length
        length /= CALLIBRATION
        width /= CALLIBRATION
        if length < 1: continue
        text = f"Length: {length:.2f} cm"
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 4, 1)
        image = cv2.putText(image, text, (x, y), FONT, 1.5, (0, 255, 0), 2, 1)
    cv2.imshow("Video", image)
    cv2.waitKey(33)
cv2.waitKey()
video.release()
