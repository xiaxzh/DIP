function [ psnr ] = PSNR( origin, target )
    origin = double(origin);
    target = double(target);
    if ndims(origin) == 3
        origin_ycbcr = rgb2ycbcr(origin);
        target_ycbcr = rgb2ycbcr(target);
        origin_y = origin_ycbcr(:, :, 1);
        target_y = target_ycbcr(:, :, 1);
    else
        origin_y = origin;
        target_y = target;
    end
    [height, width] = size(origin_y);
%     MSE = sum(sum((origin(:,:)-target(:,:)).^2))/(height*width);
    sum = 0.0;
    for i = 1:height
        for j = 1:width
            sum = sum + (origin_y(i,j)-target_y(i,j))^2;
        end
    end
    MSE = sum/(height*width);
    psnr = 20*log10(255/sqrt(MSE));
end
