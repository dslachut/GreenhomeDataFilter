function z = dCovCompute(iname,oname)
    
    X = csvread(iname);
    
    [len,wid] = size(X)
    
    x = X(:,1:wid-1)
    y = X(:,wid)
    
    fid = fopen(oname,'w')
    
    for vecWid=1:wid-1,
        c = combntns(1:wid-1,vecWid)
        [cl,cw]=size(c)
        for l = 1:cl
            vect = []
            for w = 1:cw
                A = x(:,c(l,w))
                vect = [vect,A]
                fprintf(fid,'%g',A)
                if w == cw
                    fprintf(fid,',')
                else
                    fprintf(fid,' ')
                end
            end
            [dCovXY, dCorXY, ts, pval, dCovXX, dCovYY] = distCovariance(vect,y)
            fprintf(fid,'%g,%g\n',dCorXY,ts)
        end
    end
    z = 0
end