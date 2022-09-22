import numpy as np
import cv2

vid1 = r"vid\project_video.mp4"
vid2 = r"vid\challenge_video.mp4"
vid3 = r"vid\harder_challenge_video.mp4"

scaleY = 1

# This set of coordinates are SPECIFICALLY tuned for vid1
Normal_Camera_Coord = np.float32([[1030, 509], [736, 444], [569, 444], [423, 509]])
Bird_eye_Coord = np.float32([[1000, 1667], [1000, 0], [0, 0], [0, 1667]])

Orange_Range_Start = np.array([10, 50, 135])
Orange_Range_End = np.array([30, 255, 255])
White_Range_Start = 200
White_Range_End = 255


def findLanes(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    OrangeMask = cv2.inRange(imgHSV, Orange_Range_Start, Orange_Range_End)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 0)
    ret, whiteMask = cv2.threshold(imgBlur, White_Range_Start, White_Range_End, cv2.THRESH_BINARY)
    whiteMask = cv2.dilate(whiteMask, np.ones((3, 3), np.uint8))

    result = OrangeMask + whiteMask
    result = cv2.erode(result, np.ones((3, 3), np.uint8))
    result = cv2.dilate(result, np.ones((13, 13), np.uint8))

    return result


def scanImg(img, start, stop, step, interval, extra=0, drawImg=None):
    result = [[0, 0]]
    for y in range(0, len(img), interval):
        isFirst = True
        startX = 0
        for x in range(start, stop, step):  # sweep across the left hand side from the center line
            if img[y, x] == 255 and isFirst:
                startX = x
                isFirst = False
            if (img[y, x] == 0 or x <= 1) and isFirst is False:
                endX = x - step
                realX = ((startX + endX) // 2) + extra
                result = np.append(result, [[realX, y]], axis=0)
                if drawImg is not None:
                    cv2.circle(drawImg, (realX, y), 10, 0, 5)
                break
    return np.delete(result, 0, 0)


def findCurvature(array):
    Rx = []
    dataX = array[:, 0]
    dataY = array[:, 1]
    pz = np.polyfit(dataX, dataY, 2)
    p2 = 2 * pz[0]

    for xPoint in dataX:
        p1 = 2 * pz[0] * xPoint + pz[1]
        r = ((1 + p1 ** 2) ** 1.5) / (30*abs(p2))
        Rx = np.append(Rx, r)

    minX = np.min(dataX)
    maxX = np.max(dataX)
    lenX = maxX - minX
    theoreticalX = np.linspace(minX, maxX, lenX)
    theoreticalY = pz[0] * theoreticalX ** 2 + pz[1] * theoreticalX + pz[2]
    theoretical = np.stack([theoreticalX, theoreticalY], axis=-1)

    return Rx.mean(), theoretical.astype(int)
