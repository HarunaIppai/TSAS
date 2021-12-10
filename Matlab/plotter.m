% For ANS By Juyi Zhang
function y_column = plotter(data, name, num)
    FollowerChange = data(2,:)-data(1,:);
    TweetChange = data(4,:)-data(3,:);
    errorplotlog(data(1,:),TweetChange,num,831,7983227,'Follower Count','Tweet Count',name);
    y_column = errorplotlog(TweetChange,FollowerChange,num,1,10000,'Tweet Count','Follower Change',name);
    %figure
    %subplot(1,2,1);
    %scatter(data(1,:),TweetChange);
    %set(gca,'xscale','log')
    %title("Follower Count Verus Tweet Count -- Weibo");
    %subplot(1,2,2);
    %scatter(TweetChange,FollowerChange);
    %title("Tweet Count Versus Follower Change -- Weibo");
    %set(gca,'xscale','log')
end

