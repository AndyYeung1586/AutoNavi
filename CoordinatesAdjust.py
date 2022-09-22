import cv2
import numpy as np

imagePath = "output/frame123.jpg"


def empty(a):
    pass


# Sliders
cv2.namedWindow("sliders")
cv2.resizeWindow("sliders", 1080, 400)
cv2.createTrackbar("BrightX", "sliders", 1, 1280, empty)
cv2.createTrackbar("TrightX", "sliders", 1, 1280, empty)
cv2.createTrackbar("TleftX", "sliders", 0, 1280, empty)
cv2.createTrackbar("BleftX", "sliders", 0, 1280, empty)
cv2.createTrackbar("botY", "sliders", 1, 720, empty)
cv2.createTrackbar("topY", "sliders", 0, 720, empty)
cv2.createTrackbar("x", "sliders", 50, 2000, empty)
cv2.createTrackbar("y", "sliders", 50, 2000, empty)
cv2.createTrackbar("scale", "sliders", 1, 10, empty)
cv2.createTrackbar("scaleY", "sliders", 100, 500, empty)


while True:

    # Sliders
    BrightX = cv2.getTrackbarPos("BrightX", "sliders")
    TrightX = cv2.getTrackbarPos("TrightX", "sliders")
    TleftX = cv2.getTrackbarPos("TleftX", "sliders")
    BleftX = cv2.getTrackbarPos("BleftX", "sliders")
    botY = cv2.getTrackbarPos("botY", "sliders")
    topY = cv2.getTrackbarPos("topY", "sliders")
    x = cv2.getTrackbarPos("x", "sliders")
    y = cv2.getTrackbarPos("y", "sliders")
    scale = cv2.getTrackbarPos("scale", "sliders")
    scaleY = cv2.getTrackbarPos("scaleY", "sliders")

    frame = cv2.imread(imagePath)

    Normal_Camera_Coord = np.float32([[1030, 509], [736, 444], [569, 444], [423, 509]])

    # Normal_Camera_Coord = np.float32([[BrightX, botY], [TrightX, topY], [TleftX, topY], [BleftX, botY]])
    Bird_eye_Coord = np.float32([[1000, 1667], [1000, 0], [0, 0], [0, 1667]])
    matrix = cv2.getPerspectiveTransform(Normal_Camera_Coord, Bird_eye_Coord)
    result = cv2.warpPerspective(frame, matrix, [x, y])

    if scale == 0:
        scale = 4
    scale /= 10.
    if scaleY == 0:
        scaleY = 100
    scaleY /= 100.

    result = cv2.resize(result, (0, 0), fx=1, fy=scaleY)
    result = cv2.resize(result, (0, 0), fx=scale, fy=scale)

    cv2.imshow("Output", result)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        print(Normal_Camera_Coord.astype(int))
        print(x, y)
        break
