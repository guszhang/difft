function x = func_sine_wave(f, Fs, N)

% Generate a simple sine wave signal

x = sin(2 * pi * f * (0:N-1) / Fs);

