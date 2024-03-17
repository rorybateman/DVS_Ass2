import cv2
import numpy as np
# Load the main image and the template image
image = cv2.imread('extracted_region.png')
main_image = cv2.imread('speed_photos/UK_20mph.jpg')
# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Create a binary mask for non-black pixels
_, mask = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)

# Find contours of non-black regions
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get the bounding box of the non-black regions
x, y, w, h = cv2.boundingRect(contours[0])

# Crop the image to focus on non-black pixels
cropped_image = main_image[y:y+h, x:x+w]

distance = real_size * focal_length / object_size_in_image


cv2.imwrite('cropped.jpg', cropped_image)