fileFolder = fullfile('./Set14');
dirOutput = dir(fullfile(fileFolder, '*.bmp'));
fileNames = {dirOutput.name}';
[count, nouse] = size(fileNames);
for cnt = 1:count
    filename = cell2mat(fileNames(cnt));
    strcat('./Set14/', filename)
    origin = imread(strcat('./Set14/', filename));
    if ndims(origin) == 2
        [height, width] = size(origin);
        
        target = bicubic(origin, floor(1/3*height), floor(1/3*width));
        imwrite(target, strcat('./temp/', filename));
        
        ret = bicubic(target, height, width);
        imwrite(ret, strcat('./Result/', filename));
        
    else
        [height, width, channel] = size(origin);

        r = origin(:, :, 1);
        g = origin(:, :, 2);
        b = origin(:, :, 3);

        tarr = bicubic(r, floor(1/3*height), floor(1/3*width));
        targ = bicubic(g, floor(1/3*height), floor(1/3*width));
        tarb = bicubic(b, floor(1/3*height), floor(1/3*width));
        target = cat(3, tarr, targ, tarb);
        imwrite(target, strcat('./temp/', filename));

        retr = bicubic(tarr, height, width);
        retg = bicubic(targ, height, width);
        retb = bicubic(tarb, height, width);
        ret = cat(3, retr, retg, retb);
        imwrite(ret, strcat('./Result/', filename));
    end

end