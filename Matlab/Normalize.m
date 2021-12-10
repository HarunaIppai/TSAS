function y_column = Normalize(A)
    y_column = zeros(length(A(:,1,1)),length(A(1,:,1)),length(A(1,1,:)));
    for i=1:length(A(:,1,1))
        for j=1:length(A(1,:,1))
            totalAmount = sum(A(i,j,:));
            y_column(i,j,:) = A(i,j,:)/totalAmount*100;
        end
    end
end