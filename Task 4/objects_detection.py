import cv2 as cv
import numpy as np
import time

THRESHOLD_AREA = 1000

def display_contours(img, img_with_contours):
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contours.sort(key=lambda contour: cv.contourArea(contour), reverse=True)

    for contour in contours[0:3]:
        area = cv.contourArea(contour)
        if area > THRESHOLD_AREA:
            cv.drawContours(img_with_contours, contour, -1, (255, 0, 255), 7)
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(img_with_contours, (x, y), (x + w, y + h), (0, 255, 0), 5)

    cv.imshow("Countours detector", img_with_contours)


def process_image(img):
    res_img = img.copy()
    
    img_blur = cv.GaussianBlur(img, (7, 7), 1)
    img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)

    img_canny = cv.Canny(img_gray, 30, 40)
    kernel = np.ones((5, 5))
    img_dil = cv.dilate(img_canny, kernel, iterations=1)

    display_contours(img_dil, res_img)

def main():
    filename = 'test_video.MOV'
    cap = cv.VideoCapture(filename)
    
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print('Couldn\'t receive a frame') 
            break

        process_image(frame)

        time.sleep(0.1)
        if cv.waitKey(1) == ord('q'):
            print('Exiting...')
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
