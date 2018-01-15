%%%%%%%%%%%%%%%%%%%%
% Step 8
% Generate the HR Image and save into "../HRImage"
%%%%%%%%%%%%%%%%%%%%

clc
clear
close all


[sf, ~] = getParameters();


fileFolder = fullfile('../temp');
dirOutput = dir(fullfile(fileFolder, '*.bmp'));
fileNames = {dirOutput.name}';
[count, ~] = size(fileNames);


loaddata = load('../Clustercenter.mat','cluster_center');
cluster_center = loaddata.cluster_center';        % to make column type

loaddata = load('../FinalRegressor.mat','coef_matrix_merged');
coef_matrix = loaddata.coef_matrix_merged;

for idx_file = 1:count
    filename = fileNames{idx_file};
    short = filename(1:end-4);
    tic;
    fn_read = filename;
    image_rgb_lr = im2double(imread(strcat('../temp/', filename)));
    if size(image_rgb_lr,3) == 3
        image_yiq_lr = RGB2YIQ(image_rgb_lr);
        image_y_lr = image_yiq_lr(:,:,1);
        image_iq_lr = image_yiq_lr(:, :, 2:3);
        image_y_hr = Reconstruct(image_y_lr, sf, cluster_center, coef_matrix);
        [h_lr, w_lr, channel] = size(image_rgb_lr);
        image_yiq_hr = zeros(sf*h_lr, sf*w_lr, channel);
        image_yiq_hr(:, :, 1) = image_y_hr;
        image_yiq_hr(:, :, 2:3) = imresize(image_iq_lr, sf);
        image_rgb_hr = YIQ2RGB(image_yiq_hr);
        imwrite(image_rgb_hr, strcat('../HRImage/', filename));
    else
        img_y_hr = Reconstruct(image_rgb_lr, sf, cluster_center, coef_matrix);
        imwrite(img_y_hr, strcat('../HRImage/', filename));
    end
    toc;
end            
