from collections import deque
import cv2 as cv
import numpy as np
import time
import os


THRESHOLD_CONTOUR_AREA = 1000
DEQUE_DEFAULT_MAX_SIZE = 32
THICKNESS_COEF = 2
# for each object we have its own set of points
points_list = [deque(maxlen=DEQUE_DEFAULT_MAX_SIZE) for _ in range(2)]
avg_points_list = [deque(maxlen=DEQUE_DEFAULT_MAX_SIZE) for _ in range(2)]


def moving_average(x, n):
    # скользящее среднее
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / n


def get_avg_pts(pts, n):
    pts_list = list(pts)
    list_x, list_y = np.array([point[0] for point in pts_list]), np.array([point[1] for point in pts_list])

    x_avg = moving_average(list_x, min(len(list_x), n))
    y_avg = moving_average(list_y, min(len(list_y), n))

    pts_avg = deque(maxlen=DEQUE_DEFAULT_MAX_SIZE)

    for i in range(len(x_avg)):
        pts_avg.append((int(x_avg[i]), int(y_avg[i])))

    return pts_avg

'''
def get_avg_pts(pts, n):
    pts_list = list(pts)
    pts_len = len(pts_list)
    list_x, list_y = np.array([point[0] for point in pts_list]), np.array([point[1] for point in pts_list])

    x_avg = moving_average(list_x, min(pts_len, n))
    y_avg = moving_average(list_y, min(pts_len, n))

    pts_avg = deque(maxlen=DEQUE_DEFAULT_MAX_SIZE)

    for i in range(pts_len):
        pts_avg.append((int(x_avg[i]), int(y_avg[i])))

    return pts_avg
'''


def draw_tracks(img, contours):
    objects_count = len(contours)

    for i in range(objects_count):
        x, y, w, h = cv.boundingRect(contours[i])
        center = (int(x + w/2), int(y + h/2))
        points_list[i].appendleft(center)
        avg_points_list[i] = get_avg_pts(points_list[i], 7)

    for pts in avg_points_list:
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            if (thickness := int(np.sqrt(64 / i + 1) * THICKNESS_COEF - THICKNESS_COEF)):
                cv.line(img, pts[i - 1], pts[i], (0, 0, 255), thickness)


def display_contours(img, img_with_contours):
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contours = [_ for _ in contours if cv.contourArea(_) > THRESHOLD_CONTOUR_AREA]
    contours.sort(key=lambda c: cv.contourArea(c))

    cv.drawContours(img_with_contours, contours, -1, (255, 0, 0), 5)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(img_with_contours, (x, y), (x + w, y + h), (0, 255, 0), 5)
    
    draw_tracks(img_with_contours, contours)

    cv.imshow('Countours detector', img_with_contours)


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
    filename = os.path.join(os.path.dirname(__file__), os.path.pardir, 'resources/test_video.MOV')
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
