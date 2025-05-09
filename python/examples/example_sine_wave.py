import numpy as np
import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from difft import difft

def func_sine_wave(f, Fs, N):
    """
    Generate a simple sine wave signal.

    Parameters:
    f (float): Frequency of the sine wave in Hz.
    Fs (float): Sampling frequency in Hz.
    N (int): Number of samples.

    Returns:
    numpy.ndarray: Generated sine wave signal.
    """
    return np.sin(2 * np.pi * f * np.arange(N) / Fs)

# Example usage

freq = 50.1
Fs = 100000
N = 8192

x = func_sine_wave(freq, Fs, N) + 0.5 * func_sine_wave(3 * freq, Fs, N)

# plot the signal
plt.figure()
plt.plot(x)
plt.title('Input Signal')
plt.xlabel('Sample Number')
plt.ylabel('Amplitude')
plt.grid()

# Perform DIFFT extraction
f, Amp, phi, dc = difft(x, Fs)

# Print the results
print(f"Base frequency: {f:.2f} Hz")

# plot ampitude of from 1..11 in Amp with bar chart
plt.figure()
plt.bar(range(1, 12), Amp[0:11])
plt.title('Amplitude of Extracted Harmonics')
plt.xlabel('Order')
plt.ylabel('Amplitude')
plt.xticks(range(1, 12))
plt.grid()
plt.show()