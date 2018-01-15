%%%%%%%%%%%%%%%%%%%%
% Step 4
% Load the features generated the last step
% Generate the cluster center using kmeans
% Save 'cluster_center' into "../Clustercenter.mat"
%%%%%%%%%%%%%%%%%%%%

clear
close all
clc

featurelength_lr = 45;
[number_patch_to_train_cluster, number_cluster] = getClusterInfo();

% load the feature used for train cluster center
loaddata = load('../preparedTrain.mat');
feature_used = loaddata.feature_for_cluster;

% train cluster
seed = RandStream('mcg16807', 'Seed', 0);
RandStream.setGlobalStream(seed);

number_iteration = 300;
opts = statset('Display', 'iter', 'MaxIter', number_iteration);
[IDX, C] = kmeans(feature_used, number_cluster, 'emptyaction', 'drop', 'options', opts);

arr_training_instance = hist(IDX, number_cluster);
[arr_training_instance_sort, IX] = sort(arr_training_instance, 'descend');
cluster_center = C(IX, :);

save('../Clustercenter.mat', 'cluster_center');

