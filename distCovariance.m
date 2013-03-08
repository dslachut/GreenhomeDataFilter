function [dCovXY, dCorXY, ts, pval, dCovXX, dCovYY] =  distCovariance(X, Y, a, R)
% Compute the distance covariane/correlation of 
% the X and Y NxP and NxQ data matrices
% As well as the p-value
% 
% Measuring and testing dependence by correlation of distances
% Gábor J. Székely, Maria L. Rizzo, and Nail K. Bakirov
% Source: Ann. Statist. Volume 35, Number 6 (2007), 2769-2794. 
% http://projecteuclid.org/DPubS?service=UI&version=1.0&verb=Display&handle=euclid.aos/1201012979
%
% Properties of distance correlation [SRB07] ::
% dCorXY = 0 iff X and Y are independent
% dCorXY = 1 => Y = a + bX*C, C an orthonormal matrix 
%
% Corollary 2 [SRB07]
% if X and Y are independent then the (normalized) ts -> Q, 
% where Q = linear combination squares of i.i.d. N(0,1) Gaussians and E[Q] =  1
% if X and Y are dependent then ts-> infty
%
% See SR09 [Brownian covariance]
% Pr[ Q >= chi-squared(1-alpha, degrees-of-freedom=1) ] <= a
% Thus, reject independence when Q > chi2(df=1, 1-alpha) 
%
% Theorem 6 in [SRB07]:: Reject independence of X and Y at the a-level if sqrt(test-statistic) >
% inverse-normal-cdf(1-a/2)
%
% Written by Dr. Kalpakis (dr.kalpakis@gmail.com), Oct 15, 2012
% 

if nargin == 2,
    a = 2;
    R = 200;
elseif nargin == 3 ,
    R = 200;
end;


n = size(X,1);
p = size(X,2);
q = size(Y,2);

if size(Y,1) ~= n, 
    fprintf('Error :: the data vectors should have the same number of items\n');
end;

% compute the pair-wise distances on the X and Y attributes
% the distance matrices could be passed in as arguments
% 
A = zeros(n,n);
B = zeros(n,n);
for i=1:n,
    for j=1:n,
        z1 = 0;
        z2 = 0;
        for k=1:p,
            z1 = z1 + abs( X(i,k) - X(j,k) ) ^ a;
            z2 = z2 + abs( Y(i,k) - Y(j,k) ) ^ a;
        end;
        A(i,j) = z1^(1/a);
        B(i,j) = z2^(1/a);
    end;
end;


avg_rowA = zeros(n,1);
avg_colA = zeros(n,1);
avg_rowB = zeros(n,1);
avg_colB = zeros(n,1);
for i=1:n,
    avg_rowA(i) = mean(A(i,:));
    avg_colA(i) = mean(A(:,i));
    avg_rowB(i) = mean(B(i,:));
    avg_colB(i) = mean(B(:,i));
end;
avg_A = mean(reshape(A,n^2,1));
avg_B = mean(reshape(B,n^2,1));

% center the distance matrices
for i=1:n,
    for j=1:n,
        A(i,j) = A(i,j) - avg_rowA(i) - avg_colA(j) + avg_A;
        B(i,j) = B(i,j) - avg_rowB(i) - avg_colB(j) + avg_B;
    end;
end;

% compute the sample distance covariance and correlation
dCovXY = 0;
dCovXX = 0;
dCovYY = 0;
for i=1:n,
    for j=1:n,
        dCovXY = dCovXY + A(i,j) * B(i,j);
        dCovXX = dCovXX + A(i,j) * A(i,j);
        dCovYY = dCovYY + B(i,j) * B(i,j);
    end;
end;
dCovXY = dCovXY / (n^2) ; 
dCovXX = dCovXX / (n^2) ; 
dCovYY = dCovYY / (n^2) ; 
if dCovXX * dCovYY < 1e-10,
    dCorXY = 0;
else
    dCorXY = dCovXY / sqrt( dCovXX * dCovYY );
    %dCorXY = sqrt( dCorXY );
end;


% compute the test statistic
% the distribution of ts is that of a quadratic form of centered Gaussian
% variables; it's normalized so that if X and Y are idndependent then ts->Q
% and Q is chi2(df=1)
%
ts = n * dCovXY / (avg_A * avg_B );

% Compute the p-value for the test statistic using R replicates
pval = NaN;
reps = zeros(R,1);
m = 0;
for r=1:R,
    dcov = 0;
    perm = randperm(n);
    for i=1:n,
        for j=1:n,
            I = perm(i);
            J = perm(j);
            dcov = dcov + A(i,j) * B(I,J);
        end;
    end;
    dcov = dcov / (n^2) ;
    reps(r) = dcov;
    if dcov >= dCovXY,
        m = m+1;
    end;
end;
pval = (m+1)/(R+1);

