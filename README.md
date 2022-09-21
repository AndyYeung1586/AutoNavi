# Autonomous Traffic Lane Detection and Curvature Estimation
The goal of this project is to detect the occupied traffic lane on a highway in real time, as well as determine the curvature of the traffic lane.
To do this, this project utilizes **OpenCV** and **NumPy** libraries to process the dashcam feed/footage. As well as using os library to manage processed data.

## Motivation
This is a final project 
As a commuter living in suburbia, travelling anywhere almost always require travelling on a highway.
And with how dangerous the condition on highway is, millions of drivers have to dedicate hours of attention from hurting themselves everyday.
While actual autonomous driving maybe decades away from reality, and actual solution to free people from traveling by car maybe near impossible from a social point of view, 
we can implement safety features on car today to make commuting experience less deadly.
This includes using on board camera system for lane tracking and keeping, which is the motivation for picking this as my final project.

## Process
### Step 1
First, by using `cv2.warpPerspective()`, we can apply a transformation matrix to the dashcam feed/footage. 
This matrix operation will "stretch and rotate" an image to a new shape depending on the transformation matrix the image was applied with.
With the help of `cv2.getPerspectiveTransform()`, we are able to get a transformation matrix that "reprojects" from the normal camera view 
to a bird-eye view of the road. This is done by feeding `cv2.getPerspectiveTransform()` 2 sets of coordinates, where the function will automatically generate the transformation matrix that convert the first set of coordinates to the second set of coordinates.
And to get an accurate transformation (or just the desired transformation), we can use `CoordinatesAdjust.py` and insert a test image, where we can find the desired coordinates to transform.
And once we "stretch" the image correctly, we can semi-accurately calculate the curvature using the transformed image.

### Step 2
Now that we have a bird-eye view of the road, we can use `cv2.inRange()` and `cv2.threshold()` to identify any orange and white lanes on the highway on each frame. 
Several techniques are used to remove noises from each frame and enhance any lanes we have identified.
Once we have clearly identified the traffic lanes on the road, we can then split the frame into a left-hand side and a right-hand side. 
This allows the computer to process each individual lane.

### Step 3
By processing the lane data, we can find the coordinates of the lane's markings, which can be used to estimate the curvature of the lane [mathematically](https://www.cuemath.com/radius-of-curvature-formula/). 
The estimated curvature of the left and right lane's markings are combined to come up with the average estimated curvature of the lane.
And by comparing the position of the lanes between the far-end of the lane and the close-end of the lane, we can determine whether the lane is turning right or left;
We can also determine how sharp the turn is.

### Step 4
Finally, the coordinates of the lane's marking are reprojected onto the normal camera view, and the user can see how well(or poorly) the program is functioning.

## Shortcoming
As this program is incredibly rudimentary, it is bounded to have many flaws/shortcomings:


1. The bird-eye view is unaware of any slope change for the upcoming road, and the curvature can be very off 
2. Sometime the lane markings are very faint and blended with the concrete road, where the system is unable to detect any white lane markings
3. Since the camera does not support High Dynamic Range, lane markings in the shadow is virtually undetectable
4. The transformation Matrix has to be perfectly tuned for the system to work; otherwise, the actual lane maybe off screen

## Contribution
This project is my final project for the First-year Innovation and Research Experience program (Spring 2021). This project is mentored by 
[Dr. Sanket](https://www.linkedin.com/in/nitinjsanket/) and [Naitri](https://www.linkedin.com/in/naitri-rajyaguru/). 
Many thanks to both two for making this possible!
