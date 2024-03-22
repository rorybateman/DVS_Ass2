clear all;
close all;
% Read the images
scene = imread('speed_photos/UK_50mph.jpg');
template = imread('Template_speeds/40.jpeg');

% Ensure the template and the scene are of the same class
if ~strcmp(class(scene), class(template))
    error('Scene and template must be of the same class.');
end

% Split the channels for both the scene and template
scene_red = scene(:,:,1);
scene_green = scene(:,:,2);
scene_blue = scene(:,:,3);

template_red = template(:,:,1);
template_green = template(:,:,2);
template_blue = template(:,:,3);

% Perform template matching on each channel
correlationOutputRed = normxcorr2(template_red, scene_red);
correlationOutputGreen = normxcorr2(template_green, scene_green);
correlationOutputBlue = normxcorr2(template_blue, scene_blue);

surf(correlationOutputRed), shading flat

% Display the correlation outputs
figure;
subplot(3, 1, 1);
imshow(correlationOutputRed, []);
title('Red Channel');
subplot(3, 1, 2);
imshow(correlationOutputGreen, []);
title('Green Channel');
subplot(3, 1, 3);
imshow(correlationOutputBlue, []);
title('Blue Channel');

% Combine the correlation results with weighted average
correlationOutput = (2 * correlationOutputRed + correlationOutputGreen + correlationOutputBlue) / 4;

% Find the top 5 peaks in the correlation output
correlationOutputLinear = correlationOutput(:);
[sortedValues, sortIndex] = sort(correlationOutputLinear, 'descend');

numPeaks = 5;
peakIndices = sortIndex(1:numPeaks);

% Initialize figure
figure;
imshow(scene);
hold on;

% Compute and draw rectangles for each peak found
for i = 1:numPeaks
    [yPeak, xPeak] = ind2sub(size(correlationOutput), peakIndices(i));
    
    % Find offset
    corr_offset = [(yPeak-size(template,1)) (xPeak-size(template,2))];
    
    % Draw rectangles
    rectangle('Position', [corr_offset(2), corr_offset(1), size(template, 2), size(template, 1)], ...
              'EdgeColor', [1-i*0.2, i*0.2, 0], 'LineWidth', 2); % Different color for each rectangle
end

% Title and release hold
title('Top 5 Detected Speed Signs in Color');
hold off;
