import cv2
import numpy as np
import matplotlib.pyplot as plt
"""Getting original mask"""
def preprocess(image,it,lower,upper,ks):

    # Create a mask to detect red color within the specified boundaries
    mask = cv2.inRange(image, lower, upper)

    # Apply the mask to extract only the red-colored region
    red_region = cv2.bitwise_and(image, image, mask=mask)

    red_region = mask

    # Define the kernel size and standard deviation
    ksize = (9, 9)  # Kernel size (has to be positive and odd) for Gaussian blur
    kernal_size = ks  # Kernel size (has to be positive and odd) for the erosion and dilation
    sigmaX = 0  # Standard deviation in X direction

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(red_region, ksize, sigmaX)

    # Define a kernel for erosion and dilation
    #kernel = np.ones((10, 10), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernal_size,kernal_size))

    # Perform erosion on the image
    img_erosion = cv2.erode(blurred_image, kernel, iterations=it)

    # Perform dilation on the image
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=it)


    return img_dilation

def mask_aply(image,mask):
    extracted_region = cv2.bitwise_and(image,image,mask = mask)
    return extracted_region
# Load the main image and the template image

def signextract(imgpath):
    main_image = cv2.imread(imgpath)
    # Define the boundaries for red color in BGR format
    lower_red = np.array([0, 0, 130], dtype=np.uint8)
    upper_red = np.array([255, 120, 255], dtype=np.uint8)
    red_mask = preprocess(main_image,8,lower_red, upper_red,5)
    #imag ebut only the red regionn remains
    red_region = mask_aply(main_image,red_mask)
    red_mask = preprocess(red_region,8,lower_red, upper_red,10)
    red_region = mask_aply(main_image,red_mask)
    return red_region


cv2.imwrite('extracted_region.png', signextract('speed_photos/UK_20mph.jpg'))

