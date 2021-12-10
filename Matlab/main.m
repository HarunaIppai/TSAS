close all
wbacf = fopen("weibo_activity.txt","r");
ttacf = fopen("twitter_activity.txt","r");
i = 0;
wbdata = fscanf(wbacf,"%d %d %d %d\n",[4 Inf]);
ttdata = fscanf(ttacf,"%d %d %d %d %f\n",[5 Inf]);
%plotter(wbdata,'Weibo',25);
%plotter(ttdata,'Twitter',25);
[y_column_wb,y_max_wb] = dataInterpreter(wbdata,50,831,7983227);
y_column_normalized_wb = Normalize(y_column_wb);
[y_column_tt,y_max_tt] = dataInterpreter(ttdata(1:4,:),50,831,7983227);
y_column_normalized_tt = Normalize(y_column_tt);