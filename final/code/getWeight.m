function [ W ] = getWeight( targetX, targetY )
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
    intX = floor(targetX);
    remX = targetX - intX;
    intY = floor(targetY);
    remY = targetY - intY;
    W = double(zeros(2,4));
    W(1, 1) = -0.5*(1+remX)^3+2.5*(1+remX)^2-4*(1+remX)+2;
    W(1, 2) = 1.5*remX^3-2.5*remX^2+1;
    W(1, 3) = 1.5*(1-remX)^3-2.5*(1-remX)^2+1;
    W(1, 4) = -0.5*(2-remX)^3+2.5*(2-remX)^2-4*(2-remX)+2;
    W(2, 1) = -0.5*(1+remY)^3+2.5*(1+remY)^2-4*(1+remY)+2;
    W(2, 2) = 1.5*remY^3-2.5*remY^2+1;
    W(2, 3) = 1.5*(1-remY)^3-2.5*(1-remY)^2+1;
    W(2, 4) = -0.5*(2-remY)^3+2.5*(2-remY)^2-4*(2-remY)+2;
end

