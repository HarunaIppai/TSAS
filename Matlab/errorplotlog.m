function y_column = errorplotlog(xin,yin,num,min,max,xlab,ylab,addt)
    logint = (log10(max)-log10(min))/num;
    x = zeros(1,num);
    for i=1:num
        x(i) = 10^(log10(min)+logint*i);
    end
    xc_storage = zeros(1,num);
    y = zeros(1,num);
    count = zeros(1,num);
    y_max = zeros(1,num);
    y_min = ones(1,num)*200;
    error = zeros(1,num);
    for i=1:length(xin)
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
                xc_storage(j) = xc_storage(j) + 1;
                break;
            end
        end
    end
    seg = 100;
    y_column = zeros(seg,num);
    y = y./xc_storage;
    for i=1:length(xin)
        for j=1:num
            if xin(i) < x(j)
                for k=1:seg
                    if(yin(i) < y_max(j)*k/seg)
                        y_column(k,j) = y_column(k,j) + 1;
                        break;
                    end
                end
                error(j) = error(j) + (yin(i) - y(j))^2/(xc_storage(j)-1);
                break;
            end
        end
    end
    error = (error.^0.5)/2;
    %min = ones(1,num)*200;
    %for i=1:num
    %    if y(i)-error(i) < 10^-3
    %        min(i) = y(i)-10^-3;
    %    end
    %end
    min = y - 10.^(2*log10(y)-log10(y+error));
    error = error+y;
    figure
    errorbar(x,y,min,error)
    set(gca,'xscale','log')
    set(gca,'yscale','log')
    xlabel(xlab)
    ylabel(ylab)
    title([xlab ' versus ' ylab ' -- ' addt])
    f = gcf;
    exportgraphics(f,[xlab ' versus ' ylab ' -- ' addt '.png'],'Resolution',600);
    figure
    hold on
    plot(1:12, y_column(1:12,1)./count(1), 'DisplayName', [xlab ' in [0,' num2str(round(x(1))) ']'])
    for i = 2:num
        plot(1:12, y_column(1:12,i)./count(i), 'DisplayName', [xlab ' in [' num2str(round(x(i-1))) ',' num2str(round(x(i))) ']'])
    end
    hold off
    legend show
    set(gca,'yscale','log')
    %set(gca,'xscale','log')
    xlabel([ylab ' Percentage'])
    ylabel('Portion of User in Current Group');
    title([ylab ' versus sample portion -- ' addt])
    %f = gcf;
    %exportgraphics(f,[ylab ' versus sample portion -- ' addt '.png'],'Resolution',600);
    figure
    plot(x,count,'r')
    set(gca,'xscale','log')
    xlabel(xlab)
    ylabel("Count of Total User in Group")
    title(['The amount of each user group in ' xlab ' -- ' addt])
    set(gca,'yscale','log')
    %f = gcf;
    %exportgraphics(f,['The amount of each user group in ' xlab ' -- ' addt '.png'],'Resolution',600);
    %fileID = fopen([xlab ' vs ' ylab ' in ' addt '.txt'],'w');
    %fprintf(fileID,'%d,',round(y_column(1:10,:)));
    %fileID2 = fopen([xlab '.txt'],'w');
    %fprintf(fileID2,'%d,',round(x));
end