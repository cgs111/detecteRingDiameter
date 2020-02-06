
from card_detection import *
from ring_detection import *
import cv2

def main():

    path = "./Images/12.JPG"
    srcImg = cv2.imread(path)
    if srcImg is None:
        print('Error opening image!')

    h, w, c = srcImg.shape
    if h > w:
        srcImg = cv2.rotate(srcImg, cv2.ROTATE_90_CLOCKWISE)
    h, w, c = srcImg.shape
    srcImg = cv2.resize(srcImg, (600, int(600 * h / w)))
    cardImg = card_detection(srcImg)
    diameter = ring_detection(cardImg)
    print("Detected Diameter:", diameter, "mm")

if __name__ == '__main__':
    main()
    cv2.waitKey(0)
    cv2.destroyAllWindows()