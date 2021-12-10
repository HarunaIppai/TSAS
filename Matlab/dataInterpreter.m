function [y_column,y_max] = dataInterpreter(data,num,min,max)
    splittedData = splitArray(data,num,min,max);
    splittedFollowerChange = splittedData(2,:,:)-splittedData(1,:,:);
    splittedTweetChange = splittedData(4,:,:)-splittedData(3,:,:);
    y_column = zeros(num,10,10);
    y_max = zeros(num,10);
    for i=1:num
        [y_column(i,:,:),y_max(i,:)] = errordatalog(squeeze(splittedTweetChange(1,:,i)),squeeze(splittedFollowerChange(1,:,i)),10,1,10000);
        close all
    end
    %First Parameter: Account Follower Count
    %Second Parameter: Quality
    %Third Parameter: Interval for follower change
    %Output: Number of User in Usergroup
end