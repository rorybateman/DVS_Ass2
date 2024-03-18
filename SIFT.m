clear all;
close all;
% Read the images
scene = imread('speed_photos/Beeswing.png');
template = imread('Template_speeds/40.jpeg');

% Convert images to grayscale
sceneGray = rgb2gray(scene);
templateGray = rgb2gray(template);

% Define a cell array with function handles for each feature detector
detectorFunctions = {@detectBRISKFeatures, @detectFASTFeatures, @detectHarrisFeatures, ...
                     @detectKAZEFeatures, @detectMinEigenFeatures, @detectMSERFeatures, ...
                     @detectORBFeatures, @detectSIFTFeatures, @detectSURFFeatures};

% Go through each detection method
for i = 1:length(detectorFunctions)
    % Detect feature points using the current detection method
    sceneFeatures = detectorFunctions{i}(sceneGray);
    templateFeatures = detectorFunctions{i}(templateGray);

    % Extract feature descriptors
    [sceneFeatures, scenePoints] = extractFeatures(sceneGray, sceneFeatures);
    [templateFeatures, templatePoints] = extractFeatures(templateGray, templateFeatures);

    % Match features using their descriptors
    featurePairs = matchFeatures(templateFeatures, sceneFeatures);

    % Retrieve locations of matched features
    matchedScenePoints = scenePoints(featurePairs(:, 2), :);
    matchedTemplatePoints = templatePoints(featurePairs(:, 1), :);

    % Estimate the geometric transform (homography) from the template to the scene
    [tform, inlierTemplatePoints, inlierScenePoints, status] = estimateGeometricTransform(...
        matchedTemplatePoints, matchedScenePoints, 'affine');

    % Display the matched points after removing outliers
    figure;
    showMatchedFeatures(template, scene, inlierTemplatePoints, inlierScenePoints, 'montage');
    title(['Matched Inlier Points using ', func2str(detectorFunctions{i})]);
end
