# DVS_Ass2

# Project Description and Achievement
System designed for real time recognition of speed limit signs using a camera. 

### Image capture
The system initiates by capturing a frames of live stills from a camera connected to the computer.

### Sign extraction
For each captured frame, the system attempts to detect the presence of speed limit signs. This is accomplished through a series of image processing steps that filter the image to isolate red-colored regions. These steps involve color filtering, erosion, dilation, and other techniques to refine the image and focus on relevant details.

### Sign Recognition
Once a potential speed limit sign is extracted from the image, the system further processes the image to isolate the numbers on the sign, which indicate the speed limit. This involves additional image processing to remove background noise and enhance the visibility of the numbers.

### Feature Matching and Identification
The processed image, now focused on the numbers of the speed limit sign, is compared against a collection of template images representing various speed limits (e.g., 20, 30, 40, 50, 60, 70 mph). Using feature detection and matching algorithms (such as SIFT, ORB, etc.), the system identifies the template that most closely matches the extracted sign, thus determining the speed limit depicted on the sign.

# 
Sign

# Instructions to run the application

# run imgcap.py
- (Print off speed limit sign)
- CTRL+C to stop the program

# Evidence of application working
(Link to video)

# Evaluation

