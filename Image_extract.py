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

NoOfpixels = (h+w)/2 # averaging the diiameter of the object

sizeofpixel = 0.0001  # in meters
object_size_in_image= NoOfpixels*sizeofpixel
real_size = 0.6  # in meters
focal_length = 0.00304  # in meters

distance = real_size * focal_length / object_size_in_image

from Signdetect import preprocess

def number_extract(image,n):
    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([75, 75, 75], dtype=np.uint8)
    mask = preprocess(image,n,lower_black, upper_black,10)
    _, bin_mask = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)
    #bin_mask = cv2.bitwise_not(bin_mask)
    #cropped_nored = cv2.bitwise_and(cropped_image,cropped_image,mask = bin_mask)
    return bin_mask

cv2.imwrite('cropped_no_text.png', cropped_image)


# Define the text, font, color, and position
text = 'distance:' + str(round(distance,3)) + 'm, ' + 'position:' + str(x+w/2) + ', ' + str(y +h/2)
font = cv2.FONT_HERSHEY_SIMPLEX
color = (150, 150, 250)  # BGR color format
position = (50, 50)
thickness = 3

# Add text to the image
cv2.putText(cropped_image, text, position, font, 1, color, thickness, cv2.LINE_4)

cv2.imwrite('cropped.png', cropped_image)