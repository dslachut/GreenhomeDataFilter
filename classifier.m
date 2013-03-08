addpath ./lssvm;

X    = csvread('site2-qd-A//Microwave-X.csv');
Y    = csvread('site2-qd-A//Microwaveclusters.csv');
Ychk = csvread('site2-qd-A//Microwaveclusters-ch.csv');
Xt   = csvread('site2-qd-A//Microwave-chX.csv');


type = 'c';
k = 'RBF_kernel';

% 'mse'
[gam,sig2] = tunelssvm({X,Y,type,[],[],k},'simplex','crossvalidatelssvm', {10,'misclass'});
[alpha,b] = trainlssvm({X,Y,type,gam,sig2,k});

%plotlssvm({X,Y,type,gam,sig2,k},{alpha,b});
%saveas(gcf,'george-lssvm.pdf')


[Yt,Zt] = simlssvm({X,Y,type,gam,sig2,k}, {alpha,b}, Xt);

fid = fopen('site2-qd-A//Microwaveprediction.txt', 'w');

for i=1:length(Ychk)
   fprintf(fid, '%g %f %f\n',Ychk(i)==Yt(i),Ychk(i),Yt(i));
end

fclose(fid);
exit;

