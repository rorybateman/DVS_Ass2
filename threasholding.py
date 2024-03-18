import numpy as np
from PIL import Image

# Load the image
img_path = 'speed_photos/Beeswing.png'
img = Image.open(img_path)
img_array = np.array(img)

# Separate the red channel
red_channel = img_array[:, :, 0]

# Threshold the red channel
threshold_value = 20 # This is an arbitrary threshold, adjust as needed
binary_image = red_channel > threshold_value

# Create a new image where only the red is visible and convert binary mask to uint8
red_visible = np.zeros_like(img_array)
red_visible[:, :, 0] = red_channel * binary_image.astype(np.uint8)

# display the image
Image.fromarray(red_visible).show()
