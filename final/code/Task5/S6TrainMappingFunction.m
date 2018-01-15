%%%%%%%%%%%%%%%%%%%%
% Step 6
% Training the coef mapping function
% Save temp coef into "../coef/"
%%%%%%%%%%%%%%%%%%%%

clear
close all
clc

[sf, sigma] = getParameters();

% Getting the count of files in "../Train"
fileFolder = fullfile('../Train');
dirOutput = dir(fullfile(fileFolder, '*.jpg'));
fileNames = {dirOutput.name}';
[count, ~] = size(fileNames);

number_files = count;

% load all HR image into hr_image_total
hr_image_total = cell(number_files,1);
for idx_image = 1:number_files
    image_read = imread(strcat('../Train/', fileNames{idx_image}));
    hr_image_total{idx_image} = im2double(rgb2gray(image_read));
end

% load all label into label_total
label_total = cell(number_files,1);
for idx_image = 1:number_files
    short = fileNames{idx_image}(1:end-4);
    loaddata = load(strcat('../label/', short),'label');
    label_total{idx_image} = loaddata.label;
end

% load all position into position_total
% load all patch_mean into mean_total
% load all feature into feature_total
position_total = cell(number_files,1);
mean_total = cell(number_files, 1);
feature_total = cell(number_files, 1);
for idx_image = 1:number_files
    short = fileNames{idx_image}(1:end-4);
    loaddata = load(strcat('../LRFeature/', short),'table_position_center', 'patch_mean', 'feature');
    position_total{idx_image} = loaddata.table_position_center;
    mean_total{idx_image} = loaddata.patch_mean;
    feature_total{idx_image} = loaddata.feature;
end

ps = 7;
featurelength_lr = 45;
featurelength_hr = (3*sf)^2;
patchtovectorindexset = [2:6 8:42 44:48];
patchsize_half = (ps-1)/2;

[~, number_cluster] = getClusterInfo();

thd_sufficient = 1000;
idx_label_start = 1;
idx_label_end = number_cluster;

warning('off','MATLAB:rankDeficientMatrix');

for idx_label = idx_label_start:idx_label_end    
    fprintf('processing %d cluster center mapping \n', idx_label)

    feature_accu = [];
    targetvalue_accu = [];
    coef_matrix = cell(1,featurelength_hr);
    idx_inst = 0;
    for idx_image = 1:number_files
        arr_match = label_total{idx_image} == idx_label;
        if nnz( arr_match ) > 0
            hr_image = hr_image_total{idx_image};

            set_match = find(arr_match);
            number_set_inst = length(set_match);
            %find the r,c by set_match;
            for idx_set_inst = 1:number_set_inst
                r = position_total{idx_image}(set_match(idx_set_inst), 1);
                c = position_total{idx_image}(set_match(idx_set_inst), 2);
                r1 = r-1;
                r2 = r+1;
                c1 = c-1;
                c2 = c+1;
                rh = (r1-1)*sf+1;
                rh1 = r2*sf;
                ch = (c1-1)*sf+1;
                ch1 = c2*sf;

                idx_inst = idx_inst + 1;
                feature_accu(idx_inst,:) = feature_total{idx_image}(set_match(idx_set_inst), :);
                patch_hr = hr_image(rh:rh1,ch:ch1);
                diff_hr = patch_hr - mean_total{idx_image}(set_match(idx_set_inst));
                targetvalue_accu(idx_inst,:) = reshape(diff_hr,[featurelength_hr,1]);
            end
        end
        if idx_inst >= thd_sufficient
            break   %break the idx_image loop
        end
    end
    %train the regressor
    A = [feature_accu ones(idx_inst,1)];
    if ~isempty(A)
        for j=1:featurelength_hr
            B = targetvalue_accu(:,j);
            coef = A\B;
            coef_matrix{j} = coef;
        end
    else
        %it is possible that the k-mean method generates 2049 cluster centers
        for j=1:featurelength_hr
            coef_matrix{j} = zeros(featurelength_lr+1,1);
        end
    end
    
    %save this regressor
    targetRegressor = sprintf('Regressor_%d.mat',idx_label);
    save(strcat('../coef/',targetRegressor),'coef_matrix');
end

