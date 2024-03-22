clear all;
close all;

% Read the image
img = imread('speed_photos/Beeswing.png');

% Separate the red channel
red_channel = img(:, :, 1);

% Threshold the red channel
threshold_value = 120; % This is an arbitrary threshold, adjust as needed
binary_image = red_channel > threshold_value;

% Convert binary_image to type double for multiplication
binary_image = double(binary_image);

% Create a new image where only the red is visible
% The result is a 3D matrix where the first plane is the red channel,
% and the other two are black.
red_visible = cat(3, red_channel .* binary_image, zeros(size(binary_image)), zeros(size(binary_image)));

% Display the image
imshow(red_visible);
