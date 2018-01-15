function [ extendingOrigin ] = extending( origin )
    [height, width] = size(origin);
    extendingOrigin = ones(height+4, width+4);
%   set the body
    extendingOrigin(3:height+2, 3:width+2) = origin(:,:);
%   set the left
    extendingOrigin(3:height+2, 1) = origin(:, 1);
    extendingOrigin(3:height+2, 2) = origin(:, 1);
%   set the right
    extendingOrigin(3:height+2, 2+width+1) = origin(:, width);
    extendingOrigin(3:height+2, 2+width+2) = origin(:, width);
%   set the top
    extendingOrigin(1, 3:width+2) = origin(1, :);
    extendingOrigin(2, 3:width+2) = origin(1, :);
%   set the bottom
    extendingOrigin(2+height+1, 3:width+2) = origin(height, :);
    extendingOrigin(2+height+2, 3:width+2) = origin(height, :);
%   set the cornor
    for i = 0:1
        for j = 0:1
            extendingOrigin(1+i, 1+j) = origin(1, 1);
            extendingOrigin(2+height+1+i, 1+j) = origin(height, 1);
            extendingOrigin(1+i, 2+width+1+j) = origin(1, width);
            extendingOrigin(2+height+1+i, 2+width+1+j) = origin(height, width);
        end
    end
end

