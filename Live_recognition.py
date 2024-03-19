import cv2
import numpy as np

template = [20,30,40,50,60]

# Load the images
#scene = cv2.imread('speed_photos/UK_20mph.jpg')
scene = cv2.imread('cropped_nored.png')


# Convert images to grayscale
pile_gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
for i in range(len(template)):
    print(str(template[i]))
    template_speed = cv2.imread('Template_speeds/'+str(template[i]) + '.jpeg')
    case_gray = cv2.cvtColor(template_speed, cv2.COLOR_BGR2GRAY)

    # Apply template matching
    result = cv2.matchTemplate(pile_gray, case_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print('max val '+ str(max_val))
    print('min val '+ str(min_val))


# Get the coordinates of the matched region
#top_left = max_loc
#bottom_right = (top_left[0] + template_speed.shape[1], top_left[1] + template_speed.shape[0])

# Draw a rectangle around the matched region
#cv2.rectangle(scene, top_left, bottom_right, (0, 255, 0), 3)

# Display the result
#cv2.imshow('Result', scene)
cv2.waitKey(0)
cv2.destroyAllWindows()