x = linspace(1, 1000, 1000);
Data = csvread("data.csv");
y = x .* Data' + 0;

mdl = fitlm(x, y)

figure
hold on
scatter(x, y)
