function [ tarImage ] = filter2d( image, filter )
    [height_image, width_image] = size(image);
    [height_filter, width_filter] = size(filter);
    extendImage = zeros(height_image + (height_filter-1) * 2, width_image + (width_filter-1) * 2);
    [height, width] = size(extendImage);
    
    % extend entity
    extendImage(height_filter:height_filter-1+height_image, width_filter:width_filter-1+width_image) = image;
    % extend horizontal border
    for i = 1:height_filter-1
        extendImage(i, width_filter:width_filter-1+width_image) = image(1,:);
        extendImage(height+1-i, width_filter:width_filter-1+width_image) = image(height_image, :);
    end
    % extend vetical border
    for i = 1:width_filter-1
        extendImage(height_filter:height_filter-1+height_image, i) = image(:, 1);
        extendImage(height_filter:height_filter-1+height_image, width+1-i) = image(:, width_image);
    end
    % extend cornor
    for i = 1:height_filter-1
        for j = 1:width_filter-1
            extendImage(i, j) = image(1, 1);
            extendImage(height_filter+height_image-1+i, j) = image(height_image, 1);
            extendImage(i, width_filter+width_image-1+j) = image(1, width_image);
            extendImage(height_filter+height_image-1+i, width_filter+width_image-1+j) = image(height_image, width_image);
        end
    end
    
    % calculating
    correlateImage = zeros(height, width);
    for x = 1:height - (height_filter-1)
        for y = 1:width - (width_filter-1)
            sum = 0.0;
            for j = 1:height_filter
                for k = 1:width_filter
                    sum = sum + filter(j, k) * extendImage(x-1+j, y-1+k);
                end
            end
            correlateImage(x+floor((height_filter-1)/2), y+floor((width_filter-1)/2)) = sum;
        end
    end
    
    % cutting
    tarImage = zeros(height_image, width_image);
    for x = 1:height_image
        for y = 1:width_image
            tarImage(x, y) = correlateImage(x+height_filter-1, y+width_filter-1);
        end
    end
end

