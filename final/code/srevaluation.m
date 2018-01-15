fileFolder = fullfile('./Set14');
dirOutput = dir(fullfile(fileFolder, '*.bmp'));
fileNames = {dirOutput.name}';
[count, ~] = size(fileNames);

for cnt = 1:count
    filename = fileNames{cnt};
    image_hr = imread(strcat('./Set14/', filename));
    if ndims(image_hr) == 3
        [height, width, channel] = size(image_hr);
        htrim = height-mod(height, 3);
        wtrim = width-mod(width, 3);
        imtrim = image_hr(1:htrim, 1:wtrim, 1:channel);
    else
        [height, width] = size(image_hr);
        htrim = height-mod(height, 3);
        wtrim = width-mod(width, 3);
        imtrim = image_hr(1:htrim, 1:wtrim);
    end
    image_sr = imread(strcat('./HRImage/', filename));
    mpsnr = PSNR(imtrim, image_sr);
    mssim = SSIM(imtrim, image_sr);
    fprintf(strcat(filename, ': psnr:%f ssim:%f \n'), mpsnr, mssim)
end