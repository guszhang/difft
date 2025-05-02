%  Perform DIFFT extraction on the input signal
%  difft.m
%  [f, Amp, phi] = difft(x, Fs, sigma)
%  x: input signal, the length of x must be a power of 2; the signal must contain at least two cycles of the fundamental component.
%  Fs: sampling frequency
%  sigma: the standard deviation of the Gaussian window
%  f: extracted base frequency
%  Amp: amplitude of the extracted harmonics
%  phi: phase of the extracted harmonics
%
%  This function is part of the DIFFT package.

%  Author: Gus Zhang
%  Email: cheng.zhang@manchester.ac.uk
%  Date: 02/05/2025
%  Version: 1.0
%  License: MIT

function [f, Amp, phi] = difft(x, Fs, sigma)
% Check if the input signal is a power of 2
if mod(log2(length(x)), 1) ~= 0
    error('The length of the input signal must be a power of 2.');
end

% calculate the bin size
binSize = Fs / length(x);

% perform a first FFT on the input signal
X = fft(x);

% calculate the amplitudes
Amp = abs(X);

% find the first peak starting from the second element
[~, peakIndex] = max(Amp(2:end));

% calculate the base frequency



