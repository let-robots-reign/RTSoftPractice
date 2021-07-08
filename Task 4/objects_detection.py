import cv2 as cv
import numpy as np
import time

THRESHOLD_AREA = 1000

def display_contours(img, img_with_contours):
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contours = [_ for _ in contours if cv.contourArea(_) > THRESHOLD_AREA]
    cv.drawContours(img_with_contours, contours, -1, (255, 0, 0), 5)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(img_with_contours, (x, y), (x + w, y + h), (0, 0, 255), 5)

    cv.imshow("Countours detector", img_with_contours)


def process_image(img):
    kernel = np.ones((2, 2), np.uint8)
    res_img = img.copy()

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.GaussianBlur(img_gray, (7, 7), 0)
    img_median_blur = cv.medianBlur(img_blur, 3)
    _, thresh = cv.threshold(img_median_blur, 180, 255, 0)
    thresh = cv.morphologyEx(thresh, cv.MORPH_GRADIENT, kernel)
    img_dilate = cv.dilate(thresh,kernel,iterations = 5)

    display_contours(img_dilate, res_img)

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
