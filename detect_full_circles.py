# detect spike black holes

# import the necessary packages
import cv2 as cv
import numpy as np

color = cv.imread('ecco_spike.jpg')
#  cv.imshow("input", color);

# Convert it to gray
gray = cv.cvtColor( color, cv.COLOR_BGR2GRAY )

# compute canny (don't blur with that image quality!!)
# edges = cv.Canny(gray, 200,20)
#  cv.imshow("canny", edges)


# Apply Boundaries - color detection to get only black circles - not bright
boundaries = [
		([0, 0, 0],[95,95,95])
]
# ([103, 86, 65],[145,133,128]) for gray 
'''
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
	#find the color and apply the mask
	mask = cv.inRange(color, lower, upper)
	output = cv.bitwise_and(color, color, mask=mask)
	#show the images
	cv.imshow("blackened", np.hstack([color, output]))
'''

# detect circles in the image
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,1,100, \
        param1=100, param2= 30, minRadius= 20, maxRadius= 50)

text_file = open("center_of_circle.txt", "w")

if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x,y,r) in circles:

        # draw the center of the circle
        #cv.circle(color, (y, x), 2, (0, 0, 255), 3)
        # collect data on a .txt file
        text_file.write('\n %d x' % x)
        text_file.write(' %d y ' % y)
        # get RGB color of middle of each circle
        (B,G,R) = color[y,x]
        text_file.write(' %d B' % B)
        text_file.write(' %d G' % G)
        text_file.write(' %d R' % R)
        # mask = np.zeros(color.shape[:2], dtype= "uint8")
        # mean = cv.mean(color, mask=mask)[:3]
        # text_file.write(" mean: {} ".format(y,x))

        # then check if it's in boundaries (black circles)
        # Remember than in Python it goes BGR and not RGB
        if (B,G,R) < (95,95,95) : # need the dark circles only
            # draw the outer circle
            cv.circle(color, (x, y), r, (0, 255, 0), 2)

text_file.close()

cv.imshow("all_circles",color)        
cv.waitKey(20000) # press a key or wait & observe for half a minute