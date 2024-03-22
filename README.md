### DVS_Ass2
# Design of Visual Systems - Speed Sign Detection Project


## Project Description and Achievement
System designed for real time recognition of speed limit signs using a camera. 

### Image capture
The system initiates by capturing a frames of live stills from a camera connected to the computer.

### Sign extraction
For each captured frame, the system attempts to detect the presence of speed limit signs. This is accomplished through a series of image processing steps that filter the image to isolate red-colored regions. These steps involve color filtering, erosion, dilation, and other techniques to refine the image and focus on relevant details.

### Sign Recognition
Once a potential speed limit sign is extracted from the image, the system further processes the image to isolate the numbers on the sign, which indicate the speed limit. This involves additional image processing to remove background noise and enhance the visibility of the numbers.

### Feature Matching and Identification
The processed image, now focused on the numbers of the speed limit sign, is compared against a collection of template images representing various speed limits (e.g., 20, 30, 40, 50, 60, 70 mph). Using feature detection and matching algorithms (such as SIFT, ORB, etc.), the system identifies the template that most closely matches the extracted sign, thus determining the speed limit depicted on the sign.

## Evidence of application working
(See video in the github)

## Instructions to run the application
- Follow the steps in the video
- run imgcap.py to run on your PC.
- Plots should popup to demonstrate it is working, close to proceed the program
- CTRL+C to interrupt and close the program

## Evaluation - Things to improve
- The system struggles with smaller signs that are further away. This is mainly because the kernal size is the same but on a smaller image, it looses a lot of the image detail. 
- We attempted to implement distance calculation but didn't quiet achieve it largely because of the problem mentioned above meaning the range of distance the sign could be is quite narrow.
- Colour and Shape Assumptions: The current system assumes that speed signs are red and of a as they are of a standard format as they are in the UK. Wouldn't be as effective with other formats of speed signs, for example in other countries.
- Optimisation: The script current utilises and run 4 different feature matching methods for each of the 6 speed signs. This is computationally expensive especially if in a real-world application with a higher frame rate. 

## Personal Statements
### Thomas
My main contribution to the final project outcome was implementing feature matching and Identification. Initially I tried to use template matching as all road signs are standardised but this wasn't suitable as the road signs are all at different angles, scales and different lighting conditions.
Also early prototyping with sign extraction and trying to implement on a raspberry pi for portable testing. 

### Rory
- Did everything else!

