import sys
import numpy as np
import cv2 as cv

THRESHOLD_AREA = 1000

def display_contours(img, img_with_countours):
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv.contourArea(contour)
        if area > THRESHOLD_AREA:
            cv.drawContours(img_with_countours, contour, -1, (255, 0, 255), 7)
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(img_with_countours, (x, y), (x + w, y + h), (0, 255, 0), 5)


def main():
    filename = 'test_pic.jpg'
    img = cv.imread(filename)
    res_img = img.copy()

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_canny = cv.Canny(img_gray, 20, 25)

    display_contours(img_canny, res_img)

    cv.imshow("Countours detector", res_img)
    cv.waitKey()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
