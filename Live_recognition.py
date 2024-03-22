import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
from Image_extract import number_extract, img_num
import pandas as pd

def live(img_path):
    #img_path = 'new test.png'
    query_img = 0
    #img_path = 'captured_image.jpg'

    templates = [20, 30, 40, 50, 60]
    while type(query_img) == int:
        try:
            query_img = img_num(img_path)  # Image from which we want to match features
            print("success")
        except:
            query_img = 1.2
            print("fail")
    #if query_img != "broken":
    #    print('')
    #else:
    #    exit()

    def keypoints_descriptors(template_filtered, query_img, detector_name):
        if hasattr(cv2, detector_name):
            detector = getattr(cv2, detector_name)()
        else:
            print(f"Detector {detector_name} not found in cv2")
            return None, None, None, None
        
        kp1, des1 = detector.detectAndCompute(template_filtered, None)
        kp2, des2 = detector.detectAndCompute(query_img, None)
        
        return kp1, des1, kp2, des2

    def match_features(des1, des2, matcher_name):
        if hasattr(cv2, matcher_name):
            matcher = getattr(cv2, matcher_name)()
        else:
            print(f"Matcher {matcher_name} not found in cv2")
            return None

        matches = matcher.knnMatch(des1, des2, k=2)
        return matches

    detectors = ['SIFT_create', 'ORB_create', 'BRISK_create', 'AKAZE_create']
    matchers = ['BFMatcher']

    best_template = None
    highest_match_count = 0

    match_results = []
    if type(query_img) != int:
        if type(query_img) != float:
            for temp in templates:
                template_speed_path = f'Template_speeds/{temp}.jpeg'
                template_filtered_path = f'Template_speeds/{temp}filtered.png'
                template_filtered = cv2.imread(template_filtered_path)
                for detec in detectors:
                    kp1, des1, kp2, des2 = keypoints_descriptors(template_filtered, query_img, detec)
                    if des1 is not None and des2 is not None:
                        for match in matchers:
                            matches = match_features(des1, des2, match)
                            if matches is not None:
                                good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

                                if len(good_matches) > highest_match_count:
                                    highest_match_count = len(good_matches)
                                    best_template = temp

                                # Append match data
                                match_results.append({
                                    'Detector': detec,
                                    'Matcher': match,
                                    'Template': temp,
                                    'Good Matches': len(good_matches)
                                })


    if best_template is not None and type(query_img) != int:
        if type(query_img) != float:
            print(f"Best match: {best_template} with {highest_match_count} good matches")
            results_df = pd.DataFrame(match_results)
            print(results_df)
    else:
        print("No good match found.")




    # Harris Corner Detection
    # Shi-Tomai Corner Detector
    # Scale-Invariant Feature Transform (SIFT)
    # Speeded-up robust features (SURF)
    # Histogram of Orientated Gradients
    # Binary Robust Independent Elementary Features (BRIEF)
    # Oriented FAST and Rotated BRIEF (ORB)


    # want to be able to input a speed limit sign and have the program output the speed limit that it corresponds to

