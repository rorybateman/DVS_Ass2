import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

from Image_extract import number_extract

template = [20,30,40,50,60]

# Load the images
cropped_image = cv2.imread('cropped_no_text.png')

scene = number_extract(cropped_image,4)
# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']



for i in range(len(template)):
    print(str(template[i]))
    template_speed = cv2.imread('Template_speeds/'+str(template[i]) + '.jpeg')
    template_filtered = number_extract(template_speed,1)
    cv2.imwrite('Template_speeds/'+str(template[i]) + 'filtered.png', template_filtered)

    # Apply template matching
    result = cv2.matchTemplate(scene, template_filtered, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print('max val '+ str(max_val))
    print('min val '+ str(min_val))

