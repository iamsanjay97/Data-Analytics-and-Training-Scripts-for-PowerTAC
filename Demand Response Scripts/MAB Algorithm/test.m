clc;
close all;
clear all;

iter=1; % 50
n= 5;  % 3 to 10
batch = 50; % 1, 2, 5, 10, 25, 50
budget = 7;  % 
no_of_rounds = 5000000;  % 50M

reg1_avg = zeros(1, no_of_rounds / batch);

for i=1:iter
    K_actual = 0.6*rand(iter, n);
    [K_est1,reg1] = online(budget, n, K_actual(i, :), batch, no_of_rounds);
    reg1_avg = reg1_avg + reg1;
end

reg1_avg = reg1_avg / iter;

plot(reg1_avg)