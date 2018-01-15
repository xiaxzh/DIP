%%%%%%%%%%%%%%%%%%%%
% Step 3
% Randomly select patchs for train cluster
% Merged the features of these patchs metioned above into 'feature_for_cluster'
% Save  into ../RandomRecode
%%%%%%%%%%%%%%%%%%%%

clear
close all
clc

featurelength_lr = 45;

% Getting the count of files in "../LRFeature"
fileFolder = fullfile('../LRFeature');
dirOutput = dir(fullfile(fileFolder, '*.mat'));
fileNames = {dirOutput.name}';
[count, ~] = size(fileNames);

% feature_total will include all the patch features in "../LRFeature"
feature_total = cell(count, 1);

% load the patch number range for each image
patch_number_per_image = zeros(count, 1);
for cnt = 1:count
    filename = fileNames{cnt};
    loaddata = load(strcat('../LRFeature/', filename));
    feature_total{cnt} = loaddata.feature;
    patch_number_per_image(cnt) = size(loaddata.feature, 1);
end

number_patch_total = sum(patch_number_per_image);

% randomly select 2e5 patch for cluster train
[number_patch_to_train_cluster, ~] = getClusterInfo();
seed = RandStream('mcg16807', 'Seed', 0);
RandStream.setGlobalStream(seed);
% sort the idx of selected patch
rand_patch_number = rand(number_patch_to_train_cluster, 1);
sort_patch_number = sort(ceil(rand_patch_number * number_patch_total), 'ascend');

% merge features for training clustercenter
feature_for_cluster = zeros(number_patch_to_train_cluster, featurelength_lr);

% imagine concatenate the patch into a list
% and access the feature file in iteration
idx_file = 1;
idx_patch_start = 1;
idx_patch_end = idx_patch_start + patch_number_per_image(idx_file)-1;

for idx_to_fill = 1:number_patch_to_train_cluster
    
    idx_patch_query = sort_patch_number(idx_to_fill);
    
    while ~(idx_patch_start <= idx_patch_query && idx_patch_query <= idx_patch_end)
        idx_file = idx_file + 1;
        idx_patch_start = idx_patch_end + 1;
        idx_patch_end = idx_patch_start + patch_number_per_image(idx_file) - 1;
    end
    
    idx_patch_number_in_image = idx_patch_query - idx_patch_start + 1;
    feature_for_cluster(idx_to_fill, :) = feature_total{idx_file}(idx_patch_number_in_image, :);
end

save('../preparedTrain.mat', 'feature_for_cluster');
