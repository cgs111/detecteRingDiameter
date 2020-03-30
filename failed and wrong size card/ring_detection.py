import cv2
import numpy as np

def ring_detection(img):

    h, w, c = img.shape
    imgCopy = img.copy()
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurImg= cv2.GaussianBlur(grayImg, (5, 5), 0)
    otsuTrethsold, otsuImage = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    circles = cv2.HoughCircles(blurImg, cv2.HOUGH_GRADIENT, 1, otsuTrethsold + 20, minRadius=30, maxRadius=250)
    if circles is not None:
       circles = np.round(circles[0, :]).astype("int")
       for (x, y, r) in circles:
           cv2.circle(imgCopy, (x, y), r, (0, 0, 255), 2)

    x1 = x - r
    y1 = y
    x2 = x + r
    y2 = y

    for i in range(0, h):
        for j in range(0, w):
            if grayImg[i, j] < 35:
                grayImg[i, j] = otsuTrethsold + 3

    sum1 = 0
    for i in range(15):
        for j in range(15):
            sum1 += grayImg[y1 - i][x1 - j]
            sum1 += grayImg[y1 + i][x1 - j]
            sum1 += grayImg[y1 - i][x1 + j]
            sum1 += grayImg[y1 + i][x1 + j]
    th1 = int(sum1 / 900) - 10
    sum2 = 0

    for i in range(15):
        for j in range(15):
            sum2 += grayImg[y2 - i][x2 - j]
            sum2 += grayImg[y2 + i][x2 - j]
            sum2 += grayImg[y2 - i][x2 + j]
            sum2 += grayImg[y2 + i][x2 + j]
    th2 = int(sum2 / 900) - 10

    t = 0
    while t < 17:
        if grayImg[y1, x1 + t] < 60 and grayImg[y1, x1 + t + 1] < 60 and grayImg[y1, x1 + t + 2] < 60:
            if grayImg[y1, x1 + t + 3] < 60 and grayImg[y1, x1 + t + 4] < 60 and grayImg[y1, x1 - t + 5] < 60:
                break
                break

        if grayImg[y1, x1 + t] > th1 and grayImg[y1, x1 + t + 1] > th1 and grayImg[y1, x1 + t + 2] > th1:
            if grayImg[y1, x1 + t + 3] > th1 and grayImg[y1, x1 + t + 4] > th1 and grayImg[y1, x1 - t + 5] > th1:
                x1 = x1 + t - 1
                break
                break
        t = t + 1

    t = 0
    while t < 17:
        if grayImg[y2, x2 - t] < 60 and grayImg[y2, x2 - t - 1] < 60 and grayImg[y2, x2 - t - 2] < 60:
            if grayImg[y2, x2 - t - 3] < 60 and grayImg[y2, x2 - t - 4] < 60 and grayImg[y2, x2 - t - 5] < 60:
                x2 = x2 - t + 1
                break
                break
        if grayImg[y2, x2 - t] > th2 and grayImg[y2, x2 - t - 1] > th2 and grayImg[y2, x2 - t - 2] > th2:
            if grayImg[y2, x2 - t - 3] > th2 and grayImg[y2, x2 - t - 4] > th2 and grayImg[y2, x2 - t - 5] > th2:
                 x2 = x2 - t + 1
                 break
                 break
        t = t + 1

    detectRadius = int((x2 - x1) / 2)
    xx = x1 + detectRadius
    cv2.circle(img, (xx, y), detectRadius, (0, 255, 0), 2)
    cv2.imshow("", img)
    card_RealWidth = 85.6
    card_RealHeight = 53.97
    d1 = card_RealWidth / w * detectRadius
    d2 = card_RealHeight / h * detectRadius
    detectDiameter = d1 + d2
    detectDiameter = round(detectDiameter, 2)
   
    return detectDiameter
