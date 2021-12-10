function [A,x] = splitArray(Ain, num, min, max)
    logint = (log10(max)-log10(min))/num;
    x = zeros(1,num);
    count = zeros(1,num);
    A = zeros(4,50000,50);
    for i=1:num
        x(i) = 10^(log10(min)+logint*i);
    end
    for i = 1:length(Ain(1,:))
        for j = 1:num
            if Ain(1,i) < x(j)
                count(j) = count(j) + 1;
                A(:,count(j),j) = Ain(:,i);
                break;
                % First Parameter Data Type
                % Second Parameter Number of Data
                % Third Parameter categorized Number
            end
        end
    end
end