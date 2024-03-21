import cv2
import numpy as np
import matplotlib.pyplot as plt
# Load the main image and the template image
from Signdetect import preprocess, mask_aply, signextract

def image_extract(image,mask):
    ''' returns a cropped image and its position on the image from which it was originally cropped'''
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # plot the image
    plt.imshow(gray_image, cmap='gray')
    plt.show()

    # Create a binary mask for non-black pixels
    _, bin_mask = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    # Find contours of non-black regions
    contours, _ = cv2.findContours(bin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Check if contours were found
    if not contours:
        print("No contours found. Check the mask image or preprocessing steps.")
        #return None, None, None, None, None  # Return None or appropriate defaults

    # Get the bounding box of the non-black regions
    x, y, w, h = cv2.boundingRect(contours[0])
    # Crop the image to focus on non-black pixels
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image,x,y,w,h

def distance_calc(x,y,h,w):
    '''returns the distance of the object from the camera and its coardinates'''
    coardinates = [x+w/2,y+h/2]
    NoOfpixels = (h+w)/2 # averaging the diameter of the object
    sizeofpixel = 0.0001  # in meters
    object_size_in_image= NoOfpixels*sizeofpixel
    real_size = 0.6  # in meters
    focal_length = 0.00304  # in meters
    distance = real_size * focal_length / object_size_in_image
    return distance, coardinates

def number_extract(image,n):
    '''converts cropped image to binary image just showing the numbers'''
    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([75, 75, 75], dtype=np.uint8)

    mask = preprocess(image,n,lower_black, upper_black,10)
    _, bin_mask = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)
    return bin_mask

def img_num(imgpath):
    '''returns the cropped image with only the numbers in it'''
    extracted_region = signextract(imgpath) # returns the red region

    source_image = cv2.imread(imgpath)

    cropped_image,x,y,w,h = image_extract(source_image,extracted_region)

    pure_number = number_extract(cropped_image,4)
    return pure_number

if __name__ == '__main__':
    img_path = 'speed_photos/UK_20mph.jpg'

    cv2.imwrite('cropped_no_text.png',img_num(img_path))


# Define the text, font, color, and position
#text = 'distance:' + str(round(distance,3)) + 'm, ' + 'position:' + str(x+w/2) + ', ' + str(y +h/2)
#font = cv2.FONT_HERSHEY_SIMPLEX
#color = (150, 150, 250)  # BGR color format
#position = (50, 50)
#thickness = 3

# Add text to the image
#cv2.putText(cropped_image, text, position, font, 1, color, thickness, cv2.LINE_4)

#cv2.imwrite('cropped.png', cropped_image)