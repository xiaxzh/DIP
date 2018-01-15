%%%%%%%%%%%%%%%%%
% Step 2
% Generate Feature from LR image  
% Save the 'feature', 'table_position_center' and 'patch_mean' into "../LRFeature"
%%%%%%%%%%%%%%%%%

clear
close all
clc

% Getting the count of files in "../LRImage"
fileFolder = fullfile('../LRImage');
dirOutput = dir(fullfile(fileFolder, '*.jpg'));
fileNames = {dirOutput.name}';
[count, ~] = size(fileNames);

patch_to_vector_exclude_corner = [2:6 8:42 44:48];
thd = 0.05;
number_smoothgradient = 200;
featurelength_lr = 45;

patchsize = 7;
patchsize_half = (patchsize-1)/2; % patch_size == 3

for cnt =1:count
    filename = fileNames{cnt};
    lr_image = im2double(rgb2gray(imread(strcat('../LRImage/', filename))));
    
    short = filename(1:end-4);
    
    [height, width] = size(lr_image);
    grad_lr = GenerateGradMatrix(lr_image);
    
    patch_idx_per_image = 0;
    patch_number_per_image = (height-patchsize+1)*(width-patchsize+1);
    feature = zeros(patch_number_per_image, featurelength_lr);      % remember the feature served for training cluster center and mapping function
    table_position_center = zeros(patch_number_per_image, 2);       % remember the position served for training cluster center and mapping funcion
    patch_mean = zeros(patch_number_per_image, 1);
    
    for r = patchsize_half+1:height-patchsize_half
        for c = patchsize_half+1:width-patchsize_half
            patch_grad_lr = grad_lr(r-2:r+2, c-2:c+2, :);
            number_underthd = nnz(abs(patch_grad_lr) <= thd);
            % if number_underthd < number_smoothgradient means that this
            % patch should not be a smooth patch
            if number_underthd < number_smoothgradient
                patch_idx_per_image = patch_idx_per_image+1;
                table_position_center(patch_idx_per_image, :) = [r, c];
                patch_lr = lr_image(r-patchsize_half:r+patchsize_half, c-patchsize_half:c+patchsize_half);
                vector_lr_exclude_corner = patch_lr(patch_to_vector_exclude_corner);
                vector_mean = mean(vector_lr_exclude_corner);
                feature(patch_idx_per_image, :) = vector_lr_exclude_corner - vector_mean;
                patch_mean(patch_idx_per_image, 1) = vector_mean; 
            end
        end
    end
    % save feature, position and patch_mean for every picture
    feature = feature(1:patch_idx_per_image, :);
    table_position_center = table_position_center(1:patch_idx_per_image, :);
    patch_mean = patch_mean(1:patch_idx_per_image, :);
    % named file by the short name of its picture shortname
    targetFilename = sprintf('%s.mat', short);
    save(strcat('../LRFeature/', targetFilename), 'feature', 'table_position_center', 'patch_mean');
end