function image_y_hr = Reconstruct(image_y_lr, sf, clustercenter, coef_matrix)
    patchsize_hr = 3*sf;
    num_predictedpixel = (patchsize_hr)^2;
    num_pixel_hr = num_predictedpixel;
    num_cluster = size(clustercenter,2);

    [h_lr, w_lr] = size(image_y_lr);
    % predict the hr image by learned regressor
    patchsize = 7;
    halfpatchsize = (patchsize - 1) /2;
    img_y_ext = wextend('2d','symw',image_y_lr,halfpatchsize);
    arr_clusteridx = zeros(h_lr*w_lr,1);
    grad_img_y_ext = GenerateGradMatrix(img_y_ext);
    patchtovectorindexset = [2:6 8:42 44:48];
    
    arr_smoothpatch = false(h_lr*w_lr,1);
    img_y_ext_bb = imresize(img_y_ext,sf);
    [h_hr_ext, w_hr_ext] = size(img_y_ext_bb);
    img_hr_ext_sum = zeros(h_hr_ext,w_hr_ext);
    img_hr_ext_count = zeros(h_hr_ext,w_hr_ext);
    
    intensity_hr = zeros(num_pixel_hr,h_lr*w_lr);
    for idx=1:h_lr*w_lr
        r = mod(idx-1,h_lr)+1;
        c = ceil(idx/h_lr);
        r1 = r+patchsize-1;
        c1 = c+patchsize-1;
        % label the smooth region
        patch_lr_grad = grad_img_y_ext(r+1:r1-1,c+1:c1-1,:);
        smooth_grad = abs(patch_lr_grad) <= 0.05;       
        if sum(smooth_grad(:)) == 200
            arr_smoothpatch(idx) = true;
        else
            patch_lr = img_y_ext(r:r1,c:c1);
            vector_lr = patch_lr(patchtovectorindexset);
            patch_lr_mean = mean(vector_lr);
            feature = vector_lr' - patch_lr_mean;   % use column vector
            % match the cluster center
            diff = repmat(feature,[1 num_cluster]) - clustercenter;
            l2normsquare = sum((diff.^2));
            [~,clusteridx] = min(l2normsquare);
            arr_clusteridx(idx) = clusteridx;
            if nnz(coef_matrix(:,:,clusteridx) > 10000)        %this is a bad coef
                arr_smoothpatch(idx) = true;
            end
            feature_hr = coef_matrix(:,:,clusteridx) * [feature;1];            
            intensity_hr_this = feature_hr + patch_lr_mean;
            intensity_hr(:,idx) = intensity_hr_this;
        end
    end
    intensity_hr(intensity_hr>1) = 1;
    intensity_hr(intensity_hr<0) = 0;
    
    % reconstruct hr image from predicted image
    dist = 2 * sf;
    for idx=1:h_lr*w_lr
        r = mod(idx-1,h_lr)+1;
        c = ceil(idx/h_lr);

        ch = (c-1)*sf +1 + dist;
        ch1 = ch + patchsize_hr -1;
        rh = (r-1)*sf+1 + dist;
        rh1 = rh+patchsize_hr-1;
        if arr_smoothpatch(idx)
            img_hr_ext_sum(rh:rh1,ch:ch1) = img_hr_ext_sum(rh:rh1,ch:ch1) + img_y_ext_bb(rh:rh1,ch:ch1);
        else
            img_hr_ext_sum(rh:rh1,ch:ch1) = img_hr_ext_sum(rh:rh1,ch:ch1) + reshape(intensity_hr(:,idx),[patchsize_hr, patchsize_hr]);
        end
        img_hr_ext_count(rh:rh1,ch:ch1) = img_hr_ext_count(rh:rh1,ch:ch1) + 1;
    end
    
    img_hr_ext_avg = img_hr_ext_sum ./ img_hr_ext_count;
    extended_boundary_hr = halfpatchsize * sf;
    image_y_hr = img_hr_ext_avg(extended_boundary_hr+1:end-extended_boundary_hr,extended_boundary_hr+1:end-extended_boundary_hr);
end