x = linspace(1, 3, 3);
y = [ 0.11 0.026 0.00004];
x_plot = linspace(0,53, 100);
fx = polyfit(x,log(y),1);
plot(x_plot,(polyval(fx,x_plot)));
grid on

