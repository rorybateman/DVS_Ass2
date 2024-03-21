import cv2
import numpy as np
import matplotlib.pyplot as plt
# Load the main image and the template image
from Signdetect import preprocess, mask_aply, signextract, find_border_indices

def image_extract(image,mask):
    ''' returns a cropped image and its position on the image from which it was originally cropped'''
    # Convert the image to grayscale
    #gray_image = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # Create a binary mask for non-black pixels
    #_, bin_mask = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    # Find contours of non-black regions
    b,t,l,r = find_border_indices(mask)
    # Check if contours were found
    # Get the bounding box of the non-black regions
    x = t[1]
    w = b[1]-t[1]
    y = l[0]
    h = r[0]-l[0]
    print("b,t,l,r")
    print(b,t,l,r)
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
    upper_black = np.array([120, 120, 120], dtype=np.uint8)

    mask = preprocess(image,n,lower_black, upper_black,2)
    _, bin_mask = cv2.threshold(mask, 20, 255, cv2.THRESH_BINARY)
    return bin_mask

def img_num(imgpath):
    '''returns the cropped image with only the numbers in it'''
    extracted_region = signextract(imgpath) # returns the red region
    source_image = cv2.imread(imgpath)
    plt.title("extracted_region", fontsize=16)
    plt.imshow(extracted_region)
    plt.show()

    cropped_image,x,y,w,h = image_extract(source_image,extracted_region)
    plt.title("cropped_image", fontsize=16)
    plt.imshow(cropped_image)
    plt.show()
    pure_number = number_extract(cropped_image,1)
    #plt.title("pure_number", fontsize=16)
    #plt.imshow(pure_number)
    #plt.show()
    return pure_number

if __name__ == '__main__':
    img_path = 'speed_photos/UK_20mph.jpg'

    #cv2.imwrite('cropped_no_text.png',img_num(img_path))

#img_path = 'plenty2.jpg'
#img_num(img_path)




# Define the text, font, color, and position
#text = 'distance:' + str(round(distance,3)) + 'm, ' + 'position:' + str(x+w/2) + ', ' + str(y +h/2)
#font = cv2.FONT_HERSHEY_SIMPLEX
#color = (150, 150, 250)  # BGR color format
#position = (50, 50)
#thickness = 3

# Add text to the image
#cv2.putText(cropped_image, text, position, font, 1, color, thickness, cv2.LINE_4)

#cv2.imwrite('cropped.png', cropped_image)