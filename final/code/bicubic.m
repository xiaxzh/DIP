function [ retImage ] = bicubic( origin, height, width )
    extendOrigin = extending(origin);
    [origin_height, origin_width] = size(origin);
    factorX = origin_height/height;
    factorY = origin_width/width;
    retImage = double(zeros(height, width));
    for x = 1:height
        for y = 1:width
            sum = 0.0;
            targetX = x*factorX;
            targetY = y*factorY;
            intX = floor(targetX);
            intY = floor(targetY);
            W = getWeight(targetX, targetY);
            for l = 1:4
                for m = 1:4
                    sum = sum + W(1, l)*W(2, m)*extendOrigin(intX+l, intY+m);
                end
            end
            retImage(x, y) = sum;
        end
    end
    retImage = uint8(retImage);
end

