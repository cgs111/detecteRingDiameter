
import cv2
import numpy as np

def card_detection(img):

    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    otsuTrethsold, otsuImage = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    imgCanny = cv2.Canny(grayImg, otsuTrethsold + 10, otsuTrethsold + 70, None, 3)

    minLineLength = 100
    maxLineGap = 30
    if otsuTrethsold > 125:
        linesP = cv2.HoughLinesP(imgCanny, 1, np.pi / 180, int(otsuTrethsold) - 10, None, minLineLength, maxLineGap)
    elif otsuTrethsold < 80:
        linesP = cv2.HoughLinesP(imgCanny, 1, np.pi / 180, int(otsuTrethsold) + 70, None, minLineLength, maxLineGap)
    else:
        linesP = cv2.HoughLinesP(imgCanny, 1, np.pi / 180, int(otsuTrethsold) + 20, None, minLineLength, maxLineGap)

    x = []
    if linesP is not None:
        for i in range(0, len(linesP)):
            pt = linesP[i][0]
            x.append(pt)

    hx = []
    wx = []
    for t in x:
        if abs(t[0] - t[2]) < abs(t[1] - t[3]):
            hx.append(t)
        else:
            wx.append(t)

    minVal = 10000
    maxVal = 0
    for i in range(0, hx.__len__()):
        if hx[i][0] < minVal:
            minVal = hx[i][0]
            left_hIdx = i
        if hx[i][2] < minVal:
            minVal = hx[i][2]
            left_hIdx = i
        if hx[i][0] > maxVal:
            maxVal = hx[i][0]
            right_hIdx = i
        if hx[i][2] > maxVal:
            maxVal = hx[i][2]
            right_hIdx = i

    minVal = 10000
    maxVal = 0
    for i in range(0, wx.__len__()):
        if wx[i][1] < minVal:
            minVal = wx[i][1]
            top_wIdx = i
        if wx[i][1] < minVal:
            minVal = wx[i][1]
            top_wIdx = i
        if wx[i][3] > maxVal:
            maxVal = wx[i][3]
            bomt_wIdx = i
        if wx[i][3] > maxVal:
            maxVal = wx[i][3]
            bomt_wIdx = i

    topLines = []
    bomtLines = []
    for i in range(0, wx.__len__()):
        slope = (wx[i][3] - wx[i][1]) / (wx[i][2] - wx[i][0])
        cons = wx[i][1] - slope * wx[i][0]
        dis1 = abs(slope * wx[top_wIdx][0] - wx[top_wIdx][1] + cons) / np.sqrt(slope * slope + 1)
        dis2 = abs(slope * wx[top_wIdx][2] - wx[top_wIdx][3] + cons) / np.sqrt(slope * slope + 1)
        if dis1 < 10.0 or dis2 < 10.0:
            topLines.append(wx[i])
        dis3 = abs(slope * wx[bomt_wIdx][0] - wx[bomt_wIdx][1] + cons) / np.sqrt(slope * slope + 1)
        dis4 = abs(slope * wx[bomt_wIdx][2] - wx[bomt_wIdx][3] + cons) / np.sqrt(slope * slope + 1)
        if dis3 < 10.0 or dis4 < 10.0:
            bomtLines.append(wx[i])

    maxtopX = 0
    mintopX = 10000
    for i in range(0, topLines.__len__()):
        if topLines[i][2] > maxtopX:
            maxtopX = topLines[i][2]
            maxtopIdx = i
    for i in range(0, topLines.__len__()):
        if topLines[i][0] < mintopX:
            mintopX = topLines[i][0]
            mintopIdx = i

    maxbomtX = 0
    minbomtX = 10000
    for i in range(0, bomtLines.__len__()):
        if bomtLines[i][2] > maxbomtX:
            maxbomtX = bomtLines[i][2]
            maxbomtIdx = i
    for i in range(0, bomtLines.__len__()):
        if bomtLines[i][0] < minbomtX:
            minbomtX = bomtLines[i][0]
            minbomtIdx = i

    def findIntersection(ax, ay, bx, by, cx, cy, dx, dy):
        a1 = by - ay
        b1 = ax - bx
        c1 = a1 * ax + b1 * ay
        a2 = dy - cy
        b2 = cx - dx
        c2 = a2 * cx + b2 * cy
        determinant = a1 * b2 - a2 * b1
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        return [x, y]

    _4Points = []
    _4Points.append(findIntersection(hx[left_hIdx][0], hx[left_hIdx][1], hx[left_hIdx][2], hx[left_hIdx][3],
                                     topLines[mintopIdx][0], topLines[mintopIdx][1], topLines[maxtopIdx][2], topLines[maxtopIdx][3]))
    _4Points.append(findIntersection(topLines[mintopIdx][0], topLines[mintopIdx][1], topLines[maxtopIdx][2], topLines[maxtopIdx][3],
                                     hx[right_hIdx][0], hx[right_hIdx][1], hx[right_hIdx][2], hx[right_hIdx][3]))
    _4Points.append(findIntersection(hx[right_hIdx][0], hx[right_hIdx][1], hx[right_hIdx][2], hx[right_hIdx][3],
                                     bomtLines[minbomtIdx][0], bomtLines[minbomtIdx][1], bomtLines[maxbomtIdx][2], bomtLines[maxbomtIdx][3]))
    _4Points.append(findIntersection(bomtLines[minbomtIdx][0], bomtLines[minbomtIdx][1], bomtLines[maxbomtIdx][2], bomtLines[maxbomtIdx][3],
                                     hx[left_hIdx][0], hx[left_hIdx][1], hx[left_hIdx][2], hx[left_hIdx][3]))

    for i in range(0, 4):
        _4Points[i][0] = int(_4Points[i][0])
        _4Points[i][1] = int(_4Points[i][1])

    cv2.line(img, (_4Points[0][0], _4Points[0][1]), (_4Points[1][0], _4Points[1][1]), (0, 255, 0))
    cv2.line(img, (_4Points[1][0], _4Points[1][1]), (_4Points[2][0], _4Points[2][1]), (0, 255, 0))
    cv2.line(img, (_4Points[2][0], _4Points[2][1]), (_4Points[3][0], _4Points[3][1]), (0, 255, 0))
    cv2.line(img, (_4Points[3][0], _4Points[3][1]), (_4Points[0][0], _4Points[0][1]), (0, 255, 0))

    cv2.circle(img, (_4Points[0][0], _4Points[0][1]), 3, (0, 0, 255), 3)
    cv2.circle(img, (_4Points[1][0], _4Points[1][1]), 3, (0, 0, 255), 3)
    cv2.circle(img, (_4Points[2][0], _4Points[2][1]), 3, (0, 0, 255), 3)
    cv2.circle(img, (_4Points[3][0], _4Points[3][1]), 3, (0, 0, 255), 3)

    def order_points(pts):

        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)

        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def four_point_transform(image, pts):

        rect = order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(pts, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    pts = np.array([_4Points[0], _4Points[1], _4Points[2], _4Points[3]], np.float32)
    result = four_point_transform(img, pts)

    return result
