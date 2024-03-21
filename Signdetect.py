import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the main image and the template image
main_image = cv2.imread('speed_photos/UK_20mph.jpg')



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

# Define the boundaries for red color in BGR format
lower_red = np.array([20, 0, 100], dtype=np.uint8)
upper_red = np.array([100, 100, 255], dtype=np.uint8)
mask = preprocess(main_image,2,lower_red, upper_red,20)


# Now black-out the area
extracted_region = cv2.bitwise_and(main_image,main_image,mask = mask)

cv2.imwrite('extracted_region.png', extracted_region)

