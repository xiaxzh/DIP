function kernel = GenerateGaussianKernel(size, sigma)
    kernel = zeros(size);
    for x=-floor(size/2):floor(size/2)
        for y=-floor(size/2):floor(size/2)
            kernel(x + ceil(size/2), y + ceil(size/2)) = (exp(- (x^2 + y^2) / (2* sigma^2 ))) / (2* sigma^2 * pi);
        end
    end
end