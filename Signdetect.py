import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the main image and the template image
main_image = cv2.imread('speed_photos/UK_20mph.jpg')
template = cv2.imread('Template speeds/20.jpeg')
"""
# Convert images to grayscale
main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

binary_mask = template_gray < t

# Perform template matching
result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# Define a threshold to find matches
threshold = 0.8
loc = np.where(result >= threshold)

# Draw rectangles around matched areas
for pt in zip(*loc[::-1]):
    bottom_right = (pt[0] + template.shape[1], pt[1] + template.shape[0])
    cv2.rectangle(main_image, pt, bottom_right, (0, 255, 0), 2)

# Display the result
cv2.imshow('Template Matching Result', main_image)
plt.imshow(binary_mask, cmap='gray')
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
"""
# Split the image into its BGR channels
blue, green, red = cv2.split(main_image)

# Set the blue and green channels to zeros
blue[:] = 0
green[:] = 0

# Merge the channels back together
red_image = cv2.merge((blue, green, red))
# Display or save the image with only the red channel
cv2.imshow('Red Channel Image', red_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
"""Getting original mask"""
def preprocess(image):

        # Define a kernel for erosion and dilation
    K = 20
    kernel = np.ones((K, K), np.uint8)
    # Perform dilation on the image
    n = 80

    left = 2*n*K
    right = 2*n*K
    top = 2*n*K
    bottom = 2*n*K
    #image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    Shiftimg = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 255))

    # Define the boundaries for red color in BGR format
    lower_red = np.array([20, 0, 100], dtype=np.uint8)
    upper_red = np.array([100, 100, 255], dtype=np.uint8)

    # Create a mask to detect red color within the specified boundaries
    mask = cv2.inRange(Shiftimg, lower_red, upper_red)

    # Apply the mask to extract only the red-colored region
    red_region = cv2.bitwise_and(Shiftimg, Shiftimg, mask=mask)


    # Define the kernel size and standard deviation
    ksize = (5, 5)  # Kernel size (has to be positive and odd)
    sigmaX = 0  # Standard deviation in X direction

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(red_region, ksize, sigmaX)

    # Define a kernel for erosion and dilation
    kernel = np.ones((10, 10), np.uint8)

    # Perform erosion on the image
    img_erosion = cv2.erode(blurred_image, kernel, iterations=2)

    # Perform dilation on the image
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=2)
    


    img_dil2 = cv2.dilate(img_dilation, kernel, iterations=n)
    # Perform erosion on the image
    img_er2 = cv2.erode(img_dil2, kernel, iterations=n)

    img_er2 = img_er2[top:img_er2.shape[0]-bottom, left:img_er2.shape[1]-right]
    img_er2 = cv2.copyMakeBorder(img_er2, 0, 80, 0, 80, cv2.BORDER_CONSTANT, value=(0, 0, 255))
    img_er2 = img_er2[80:img_er2.shape[0], 80:img_er2.shape[1]]
    return img_er2

extract_img = preprocess(main_image)
# Display or further analyze the extracted red-colored region
extract_img = cv2.cvtColor(extract_img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(extract_img, 50, 255, cv2.THRESH_BINARY)

 
# Now black-out the area of logo in ROI
extracted_region = cv2.bitwise_and(main_image,main_image,mask = mask)



cv2.imshow('Dilation', extracted_region)
#cv2.imshow('Dilation', extract_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
