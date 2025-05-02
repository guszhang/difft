freq = 50.1;
fs = 100000;
N = 8192;

x = func_sine_wave(freq, fs, N) + 0.5*func_sine_wave(3*freq, fs, N);

figure;
plot(x);

[f, Amp, Phi]=difft(x, fs);
disp(f);
figure;
bar(1:11, Amp(1:11));
pause;