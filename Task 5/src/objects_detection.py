from collections import deque
import cv2 as cv
import numpy as np
import time
import os
import json

THRESHOLD_CONTOUR_AREA = 1000  # пороговая площадь объекта - не следим за объектами с меньшей площадью
DEQUE_DEFAULT_MAX_SIZE = 32  # макс. размер дека с точками объектов
THICKNESS_COEF = 2  # толщина линии траектории

# BGR
BLUE_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (0, 0, 255)


def moving_average(arr, n):
    # скользящее среднее
    cumsum = np.cumsum(np.insert(arr, 0, 0)) 
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


def draw_tracks(img, contours, points_list, avg_points_list):
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
                cv.line(img, pts[i - 1], pts[i], RED_COLOR, thickness)


def get_contours(img, img_with_contours):
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contours = [_ for _ in contours if cv.contourArea(_) > THRESHOLD_CONTOUR_AREA]
    contours.sort(key=lambda c: cv.contourArea(c))

    cv.drawContours(img_with_contours, contours, -1, BLUE_COLOR, 5)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(img_with_contours, (x, y), (x + w, y + h), GREEN_COLOR, 5)

    return img_with_contours, contours


def process_image(img):
    kernel = np.ones((2, 2), np.uint8)

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.GaussianBlur(img_gray, (7, 7), 0)
    img_median_blur = cv.medianBlur(img_blur, 3)
    _, thresh = cv.threshold(img_median_blur, 180, 255, 0)
    thresh = cv.morphologyEx(thresh, cv.MORPH_GRADIENT, kernel)
    img_dilate = cv.dilate(thresh, kernel, iterations = 5)

    return img_dilate


def main():
    filename = os.path.join(os.path.dirname(__file__), os.path.pardir, 'resources/test_video.MOV')
    cap = cv.VideoCapture(filename)

    # for each object we have its own set of points and its own trajectory
    objects_count = 0
    points_list, avg_points_list = [], []

    frames_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print('Couldn\'t receive a frame') 
            break

        img = process_image(frame) # preprocessed image
        img_with_contours, contours = get_contours(img, frame) # drawing contours

        # if we detect more objects, we need to draw more trajectories
        contours_count = len(contours)
        if contours_count > objects_count:
            for _ in range(contours_count - objects_count):
                points_list.append(deque(maxlen=DEQUE_DEFAULT_MAX_SIZE))
                avg_points_list.append(deque(maxlen=DEQUE_DEFAULT_MAX_SIZE))
                objects_count = contours_count

        draw_tracks(img_with_contours, contours, points_list, avg_points_list)

        cv.imshow('Countours detector', img_with_contours)

        time.sleep(0.1)

        # publishing coordinates every 10 frames
        frames_count += 1
        if frames_count % 10 == 0:
            coords_list = []
            for i in range(len(points_list)):
                if len(points_list[i]) > 1 and len(avg_points_list[i]) > 1:
                    # [i] - index of points' deque; [0] - first point of the deque; [0] or [1] - x or y of the point
                    coords = {
                        'x': points_list[i][0][0], 
                        'y': points_list[i][0][1],
                        'corrected x': avg_points_list[i][0][0], 
                        'corrected y': avg_points_list[i][0][1]
                    }
                    coords_list.append(coords)

                # publish data
                if coords_list: 
                    print(json.dumps({'coords': coords_list}))

        if cv.waitKey(1) == ord('q'):
            print('Exiting...')
            break
    
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
