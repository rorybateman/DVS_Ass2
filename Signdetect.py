import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
"""Getting original mask"""
def preprocess(image,it,lower,upper,ks):
    '''
    Colour filtering and preprocessing of the image
    '''
    # Create a mask to detect red color within the specified boundaries
    mask = cv2.inRange(image, lower, upper)
    ret, mask = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


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
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    img_erosion = cv2.erode(blurred_image, kernel2, iterations=1)



    # Perform erosion on the image
    img_erosion = cv2.erode(img_erosion, kernel, iterations=it)

    # Perform dilation on the image
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=it)


    return img_dilation

def mask_aply(image,mask):
    '''Applies the mask to the image and returns the extracted region'''
    extracted_region = cv2.bitwise_and(image,image,mask = mask)
    return extracted_region
# Load the main image and the template image

def signextract(imgpath):
    ''' 
    Extracts red-coloured signs from an image using a series of preprocessing steps
    
    Returns:
    - red_region (np.array): An image array with only the extracted red regions visable, rest of the image masked out
    '''
    main_image = cv2.imread(imgpath)

    # DEBUGGING: Display the main image
    #plt.imshow(cv2.cvtColor(main_image, cv2.COLOR_BGR2RGB))
    #plt.show()

    # Define the boundaries for red color in BGR format
    lower_red = np.array([0, 0, 170], dtype=np.uint8)
    upper_red = np.array([120, 110, 255], dtype=np.uint8)

    # too sensitive
    # lower_red = np.array([0, 0, 110], dtype=np.uint8)
    # upper_red = np.array([255, 120, 255], dtype=np.uint8)

    # Create a mask to detect red color within the specified boundaries
    red_mask = preprocess(main_image,5,lower_red, upper_red,3)
    #plt.imshow(cv2.cvtColor(red_mask, cv2.COLOR_BGR2RGB))
    #plt.show()
    red_mask = cv2.bitwise_not(red_mask)
    ret, red_mask = cv2.threshold(red_mask, 50, 255, cv2.THRESH_BINARY)
    #red_region = mask_aply(main_image,red_mask)
    

    return red_mask 

def find_border_indices(mask_array):
    arr = np.array(mask_array, dtype=np.uint8)
    array_width = arr.shape[0]
    array_height = arr.shape[1]
    """
    Find the indices of 1's closest to the top, bottom, right, and left sides of the array.
    
    Args:
        arr (numpy.ndarray): A 2D array of 0's and 1's.
        
    Returns:
        dict: A dictionary containing the indices of the 1's closest to each side.
    """
    top_idx = [0,40]
    bottom_idx = [array_height-100,90]
    right_idx = [20,array_width-100]
    left_idx = [50,10]
    x = 0
    y = 0
    top_y = 0
    top_x = 0
    bottom_y = array_height
    bottom_x = array_width
    for x in range(array_width):
        for y in range(array_height):
            # Check if the current index is closer to the top
            if arr[x,y] > 0:
                if y > top_y :
                    top_idx = (x, y)
                    top_y = y
                # Check if the current index is closer to the bottom
                if y < bottom_y:
                    bottom_idx = (x, y)
                    bottom_y = y
                # Check if the current index is closer to the left
                if x > top_x:
                    right_idx = (x, y)
                    top_x = x
                # Check if the current index is closer to the right
                if x < bottom_x:
                    left_idx = (x, y)
                    bottom_x = x
        
    return top_idx, bottom_idx,left_idx,right_idx


#img_path = 'captured_image.jpg'
#x = signextract(img_path)
#b,t,l,r = find_border_indices(x)

#plt.imshow(x)
#plt.show()