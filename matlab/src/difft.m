%  Perform DIFFT extraction on the input signal
%  difft.m
%  [f, Amp, phi, dc] = difft(x, Fs, sigma)
%  x: input signal, the length of x must be a power of 2; the signal must contain at least two cycles of the fundamental component.
%  Fs: sampling frequency
%  sigma: the standard deviation of the Gaussian window
%  f: extracted base frequency
%  Amp: amplitude of the extracted harmonics
%  phi: phase of the extracted harmonics
%  dc: DC component of the input signal
%
%  This function is part of the DIFFT package.

%  Author: Gus Zhang
%  Email: cheng.zhang@manchester.ac.uk
%  Date: 02/05/2025
%  Version: 1.0
%  License: MIT

function [f, Amp, phi, dc] = difft(x, Fs, sigma)

% generate a Gaussian window
if nargin < 3
    sigma = 0.25; % default value for sigma
end

% Check if the input signal is a power of 2
if mod(log2(length(x)), 1) ~= 0
    error('The length of the input signal must be a power of 2.');
end

% reconstruct the time series
t = (0:length(x)-1)/Fs;

% retain the original signal
x_orig = x;

% remove the DC component
x = x - mean(x);

w = exp(-(((0:length(x)-1) - length(x)/2)./(sigma*length(x)/2)).^2/2);

% apply the Gaussian window to the input signal
x = x .* w;

% calculate the bin size
binSize = Fs / length(x);

% perform a first FFT on the input signal
X = fft(x);

% calculate the amplitudes
fast_extract_amp = abs(X);

% find the first peak starting from the second element
[~, peakIndex] = max(fast_extract_amp(2:end));

% calculate the base frequency
f = (peakIndex + (log(fast_extract_amp(peakIndex+1)/fast_extract_amp(peakIndex-1))/log(fast_extract_amp(peakIndex).^2/fast_extract_amp(peakIndex-1)/fast_extract_amp(peakIndex+1))/2)-1) * binSize;

% calculate the round down number of cycles
roundDownCycles = floor(length(x) / (Fs / f));

% calcualte the new sampling frequency
Fs_new = 1/((roundDownCycles / f) / length(x));

% calcualte the number of bins per base frequency
numBins = round(f / (Fs_new / length(x)));

% new time series
t_new = (0:length(x)-1)/Fs_new;

% linear interpolation
x = interp1(t, x_orig, t_new);

% perform a second FFT on the input signal
X = fft(x);

% calculate the amplitudes
fast_extract_amp = abs(X);

dc = fast_extract_amp(1);

% fold and scale the amplitudes
Amp = fast_extract_amp(1+numBins:numBins:length(x)/2) * 2 / length(x);

% calculate the phase
phi = angle(X(1+numBins:numBins:length(x)/2));
