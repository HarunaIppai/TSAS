function [y_column,y_max] = errordatalog(xin,yin,num,min,max)
    logint = (log10(max)-log10(min))/num;
    x = zeros(1,num);
    for i=1:num
        x(i) = 10^(log10(min)+logint*i);
    end
    y = zeros(1,num);
    count = zeros(1,num);
    y_max = zeros(1,num);
    y_min = ones(1,num)*200;
    for i=1:length(xin)
        if xin(i) == 0
            continue
        end
        for j=1:num
            if xin(i) < x(j)
                %outputarray = ["At index of" i "the value reads" xin(i) "which we will select" x(j) "and the y value becomes" yin(i)];
                %disp(outputarray);
                count(j) = count(j) + 1;
                y(j) = y(j) + yin(i);
                if yin(i) > y_max(j)
                    y_max(j) = yin(i);
                elseif yin(i) < y_min(j)
                    y_min(j) = yin(i);
                end
                break;
            end
        end
    end
    seg = 100;
    y_column = zeros(seg,num);
    for i=1:length(xin)
        if xin(i) == 0
            continue
        end
        for j=1:num
            if xin(i) < x(j)
                for k=1:seg
                    if(yin(i) < y_max(j)*k/seg)
                        y_column(k,j) = y_column(k,j) + 1;
                        break;
                    end
                end
                break;
            end
        end
    end
    y_column = y_column(1:10,:);
    %First Parameter: Difference From y_max
    %fileID = fopen([xlab ' vs ' ylab ' in ' addt '.txt'],'w');
    %fprintf(fileID,'%d,',round(y_column(1:10,:)));
    %fileID2 = fopen([xlab '.txt'],'w');
    %fprintf(fileID2,'%d,',round(x));
end