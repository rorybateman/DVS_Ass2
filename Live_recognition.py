import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

from Image_extract import number_extract, img_num

img_path = 'speed_photos/UK_20mph.jpg'

template = [20,30,40,50,60]

# for temp in template:
#     template_speed = cv2.imread('Template_speeds/'+str(temp) + '.jpeg')
#     #template_filtered = number_extract(template_speed,1)
#     template_filtered = cv2.imread('Template_speeds/'+str(temp) + 'filtered.png')

template_speed = cv2.imread('Template_speeds/20.jpeg')
template_filtered = cv2.imread('Template_speeds/20filtered.png')

query_img = img_num(img_path)  # Image from which we want to match features

#(Structural similarity?) (SSIM)

def keypoints_descriptors(template, query_img, detector_name):
    if hasattr(cv2, detector_name):
        detector = getattr(cv2, detector_name)()
    else:
        print(f"Detector {detector_name} not found in cv2")
        return
    
    # Find the keypoints and descriptors with detector
    kp1, des1 = detector.detectAndCompute(template,None)
    kp2, des2 = detector.detectAndCompute(query_img,None)
    
    # return the keypoints and descriptors
    return kp1, des1, kp2, des2

def match_features(template, query_img, matcher_name):
    if hasattr(cv2, matcher_name):
        matchor = getattr(cv2, matcher_name)()
    else:
        print(f"Matchor {matcher_name} not found in cv2")
        return
    matches = matchor.knnMatch(des1,des2,k=2)

detectors = ['SIFT_create', 'ORB_create']
matchers = ['BFMatcher']

for detec in detectors:
    print(detec)
    keypoints_descriptors(template_filtered, query_img, detec)
    for match in matchers:
        print(match)
        match_features(template_filtered, query_img, match)








# After obtaining the keypoints and descriptors, we can match them using a feature mapper
# initialise Brute Force Matcher
bf = cv2.BFMatcher()

# Match descriptors
matches = bf.knnMatch(des1,des2,k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

# Draw matches
# matching_result = cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#img3 = cv2.drawMatches(template_filtered,kp1,img_num(img_path),kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
img3 = cv2.drawMatchesKnn(template_filtered, kp1, query_img, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display the result

plt.imshow(img3), plt.show()

# scene = img_num(img_path)
# # All the 6 methods for comparison in a list


# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#  'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']



# for i in range(len(template)):
#     print(str(template[i]))
#     template_speed = cv2.imread('Template_speeds/'+str(template[i]) + '.jpeg')
#     template_filtered = number_extract(template_speed,1)
#     cv2.imwrite('Template_speeds/'+str(template[i]) + 'filtered.png', template_filtered)

def Harris

# Harris Corner Detection
# Shi-Tomai Corner Detector
# Scale-Invariant Feature Transform (SIFT)
# Speeded-up robust features (SURF)
# Histogram of Orientated Gradients
# Binary Robust Independent Elementary Features (BRIEF)
# Oriented FAST and Rotated BRIEF (ORB)

