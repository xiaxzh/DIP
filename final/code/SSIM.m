function [ ssim ] = SSIM ( img1, img2 )
    window = GenerateGaussianKernel(11, 1.5);
    img1 = double(img1(:, :, 1));
    img2 = double(img2(:, :, 1));
    C1 = (0.01*255)^2;
    C2 = (0.03*255)^2;
    window = window/sum(sum(window));
    mu1 = filter2d(img1, window);
    mu2 = filter2d(img2, window);
    mu1_sq = mu1.^2;
    mu2_sq = mu2.^2;
    mu1_mu2 = mu1.*mu2;
    sigma1_sq = filter2d(img1.^2, window) - mu1_sq;
    sigma2_sq = filter2d(img2.*img2, window) - mu2_sq;
    sigma12 = filter2d(img1.*img2, window) - mu1_mu2;
    ssim_map = ((2*mu1_mu2 + C1).*(2*sigma12 + C2))./((mu1_sq + mu2_sq + C1).*(sigma1_sq + sigma2_sq + C2));
    ssim = mean2(ssim_map);
end

