import os
import cv2
import numpy as np
import property as p

# ######################## Setups [I] ###########################
if os.path.exists("./output") is False:
    os.mkdir("./output")
else:
    for f in os.listdir("./output"):
        os.remove(os.path.join("./output", f))

cap = cv2.VideoCapture(p.vid1)
frm = 0

# image transformation from normal camera view to bird-eye view and vice versa
matrix = cv2.getPerspectiveTransform(p.Normal_Camera_Coord, p.Bird_eye_Coord)
matrixNew = cv2.getPerspectiveTransform(p.Bird_eye_Coord, p.Normal_Camera_Coord)


while True:
    success, vidO = cap.read()
    Original_Video = np.copy(vidO)

    vid = cv2.warpPerspective(vidO, matrix, [800, 2000])
    vid = cv2.resize(vid, (0, 0), fx=1, fy=p.scaleY)

    # ######################## Identify, Record, and Draw Lane [1] ###########################
    Lanes = p.findLanes(vid)

    halfX = len(Lanes[0]) // 2

    leftLane = Lanes[:, 0:halfX]
    rightLane = Lanes[:, halfX:]

    # the interval in the y-axis to sweep across the x-axis for detecting and recording traffic lane
    intervalY = 45
    step = 4
    leftCoord = p.scanImg(leftLane, halfX-1, 0, -step, intervalY)
    rightCoord = p.scanImg(rightLane, 0, halfX, step, intervalY, extra=halfX)

    # ######################## Finding Radius of Curvature [2] ###########################
    text = "UNKNOWN"
    if len(rightCoord) > 3 and len(leftCoord) > 3:
        left_Radius, leftCoordNew = p.findCurvature(leftCoord)
        right_Radius, rightCoordNew = p.findCurvature(rightCoord)
        Average_Radius = (left_Radius + right_Radius) // 2

        if (rightCoord[-1, 0] - rightCoord[0, 0]) < 0 and (leftCoord[-1, 0] - leftCoord[0, 0]) < 0:
            text = "Turning Right"
        elif (rightCoord[-1, 0] - rightCoord[0, 0]) > 0 and (leftCoord[-1, 0] - leftCoord[0, 0]) > 0:
            text = "Turning Left"

        if Average_Radius > 3000:
            Average_Radius = 0
            text = "Moving Straight"

        cv2.putText(vidO, "Estimated radius = " + str(int(Average_Radius)) + "ft", (50, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)

    # ######################## Re-project Data Points [3] ###########################
        coord = np.append(leftCoord, np.flip(rightCoord, axis=0), axis=0)

        cv2.polylines(vid, [coord], True, (255, 0, 255), 14)

        # coord[:, 1] = coord[:, 1]/p.scaleY  # rescale the y axis back to its original
        coord = np.array([coord], dtype=np.float32)
        cordOutput = cv2.perspectiveTransform(coord, matrixNew)
        cordOutput = np.array(cordOutput[0, :, :], int)
        cv2.polylines(vidO, [cordOutput], True, (255, 0, 255), 4)
    else:
        print("I'm Not Ok!")

    cv2.putText(vidO, text, (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 1)

    # ######################## Output Video [4] ###########################
    result = Lanes
    cv2.imwrite(r"output\frame" + str(frm) + ".jpg", result)
    frm += 1

    # scale = 1
    # result = cv2.resize(result, (0, 0), fx=scale, fy=scale)
    cv2.imshow("result", result)

    # ######################## Break Loop [5] ###########################
    if cv2.waitKey(1) == ord('q'):
        break
