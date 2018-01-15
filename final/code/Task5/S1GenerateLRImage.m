%%%%%%%%%%%%%%%%%
% Step 1
% Generate LR image from HR image as the size of LR is determinded by sf  
% Save the LR image into "../LRImage"
%%%%%%%%%%%%%%%%%

clear
close all
clc

% Getting the count of files in "../Train"
fileFolder = fullfile('../Train');
dirOutput = dir(fullfile(fileFolder, '*.jpg'));
fileNames = {dirOutput.name}';
[count, ~] = size(fileNames);

% use a universe interface
[sf, sigma] = getParameters();


for cnt = 1:count
    filename = fileNames{cnt};
    hr_image = imread(strcat('../Train/', filename));

    % determind lr size minus the extra pixel 
    [height, width, channel] = size(hr_image);
    htrim = height-mod(height, sf);
    wtrim = width-mod(width, sf);
    imtrim = hr_image(1:htrim, 1:wtrim, 1:channel);
    h_lr = htrim/sf;
    w_lr = wtrim/sf;
    
    % since sf == 3
    use the bicubic completed by myself
    kernelsize = ceil(sigma*3) * 2 + 1;
    kernel = GenerateGaussianKernel(kernelsize, sigma);
    blurimg = zeros(htrim, wtrim, channel);
    for i = 1:channel
        blurimg(:, :, i) = filter2d(imtrim(:, :, i), kernel);
    end
    lrimg = uint8(imresize(blurimg, 1/sf, 'nearest'));
    
    % lrimg = uint8(zeros(h_lr, w_lr, channel));
    % for i = 1:channel
    %     lrimg(:, :, i) = bicubic(imtrim(:, :, i), h_lr, w_lr);
    % end
    
    % store the lr_img to ../lRImage
    imwrite(lrimg, strcat('../LRImage/', filename));
end
