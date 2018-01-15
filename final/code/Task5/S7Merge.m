%%%%%%%%%%%%%%%%%%%%
% Step 7
% Merge the coef generated from 'TrainMappingFunction'
% Save 'label' into "../label"
%%%%%%%%%%%%%%%%%%%%

clear
close all
clc

% Getting the filename for each iamge in "../LRImage"
fileFolder = fullfile('../coef');
dirOutput = dir(fullfile(fileFolder, '*.mat'));
fileNames = {dirOutput.name}';
[count, ~] = size(fileNames);

featurelength_lr = 45;
featurelength_hr = 81; % (lr_patch_half * sf)^2 == (3*3)^2 == 81
[~, number_cluster] = getClusterInfo();

coef_matrix_merged = zeros(featurelength_hr, featurelength_lr + 1, number_cluster);

for cnt = 1:count
    fprintf('merged %d cluster mapping \n', cnt)
    filename = cell2mat(fileNames(cnt));
    loaddata = load(strcat('../coef/', filename));
    coef_matrix = loaddata.coef_matrix;
    for target_length_hr = 1: featurelength_hr
        coef_matrix_merged(target_length_hr, :, cnt) = coef_matrix{target_length_hr};
    end
end

save('../FinalRegressor.mat', 'coef_matrix_merged');