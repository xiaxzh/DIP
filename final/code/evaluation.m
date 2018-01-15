fileFolder = fullfile('./Set14');
dirOutput = dir(fullfile(fileFolder, '*.bmp'));
fileNames = {dirOutput.name}';
[count, nouse] = size(fileNames);
for cnt = 1:count
    filename = cell2mat(fileNames(cnt));
    origin = imread(strcat('./Set14/', filename));
    target = imread(strcat('./Result/', filename));

    mpsnr = PSNR(origin, target);
    mssim = SSIM(origin, target);
    % stdpsnr = psnr(targetY, originY);
    % stdssim = ssim(target, origin);
    fprintf(strcat(filename, ': psnr:%f ssim:%f \n'), mpsnr, mssim)
    % stdresult = sprintf('stdpsnr : %f', stdpsnr)
end