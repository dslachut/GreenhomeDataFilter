% distance correlation
 
n = 20;
p = 2;
q = 2;

% Distance function to use:: Euclidean norm raised to the power of a
% Number of replicates to use in estimating the p-value: R
a = 1.5;
R = 200;

rng('default');
X =  rand(n,p);
Y = rand(n,q);

Y =  log( X + X .^ 2 );
I = [1:ceil(n/2)];
Y(I,:) = X(I,:) .^ 2;
%Y(I,:) = rand(length(I), q);

[dCovXY, dCorXY, ts, pval, dCovXX, dCovYY ] = distCovariance(X, Y, a, R);
fprintf('distance cov^2=%12.6f cor=%8.6f pvalue=%16.6f ts=%8.6f\n', dCovXY, dCorXY, pval, ts);
fprintf('X and Y are independent iff cor -> 0\n');
fprintf('Reject the null hypothesis[X,Y are Independent] at the alpha level if p-val <= alpha\n');

figure(1);
msg = sprintf('Distance correlation dCorr=%8.6f at p-value=%8.6f test-statistic=%8.6f', dCorXY, pval, ts);
scatter(X(:,1),Y(:,1));
xlabel('X(:,1)');
ylabel('Y(:,1)');
title(msg);

%MINE(X,Y,'testABC');


