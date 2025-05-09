import numpy as np
from scipy import interpolate

def difft(x: np.ndarray, Fs: float, sigma: float = 0.25) -> tuple:
    """
    Perform DIFFT extraction on the input signal.
    
    Args:
        x (np.ndarray): Input signal, length must be a power of 2
        Fs (float): Sampling frequency
        sigma (float, optional): Standard deviation of Gaussian window. Defaults to 0.25.
    
    Returns:
        tuple: (f, Amp, phi, dc)
            f (float): Extracted base frequency
            Amp (np.ndarray): Amplitude of the extracted harmonics
            phi (np.ndarray): Phase of the extracted harmonics
            dc (float): DC component of the input signal
    
    Raises:
        ValueError: If input signal length is not a power of 2
    """
    # Check if input length is power of 2
    if not np.log2(len(x)).is_integer():
        raise ValueError('The length of the input signal must be a power of 2.')

    # Generate time series
    t = np.arange(len(x)) / Fs
    
    # Store original signal
    x_orig = x.copy()
    
    # Remove DC component
    x = x - np.mean(x)
    
    # Generate Gaussian window
    n = np.arange(len(x))
    w = np.exp(-((n - len(x)/2)/(sigma*len(x)/2))**2/2)
    
    # Apply Gaussian window
    x = x * w
    
    # Calculate bin size
    bin_size = Fs / len(x)
    
    # First FFT
    X = np.fft.fft(x)
    
    # Calculate amplitudes
    fast_extract_amp = np.abs(X)
    
    # Find the first local peak (excluding DC)
    for i in range(1, len(fast_extract_amp) - 1):
        if fast_extract_amp[i] > fast_extract_amp[i - 1] and fast_extract_amp[i] > fast_extract_amp[i + 1]:
            peak_index = i
            break
    else:
        raise ValueError("No local peak found in the spectrum.")
    
    # Calculate base frequency using interpolation
    log_ratio = np.log(fast_extract_amp[peak_index+1]/fast_extract_amp[peak_index-1])
    log_term = np.log(fast_extract_amp[peak_index]**2/(fast_extract_amp[peak_index-1]*fast_extract_amp[peak_index+1]))
    f = (peak_index + log_ratio/log_term/2) * bin_size
    
    # Calculate round down number of cycles
    round_down_cycles = np.floor(len(x) / (Fs / f))
    
    # Calculate new sampling frequency
    Fs_new = 1/((round_down_cycles / f) / len(x))
    
    # Calculate number of bins per base frequency
    num_bins = round(f / (Fs_new / len(x)))
    
    # New time series
    t_new = np.arange(len(x)) / Fs_new
    
    # Linear interpolation
    interpolator = interpolate.interp1d(t, x_orig)
    x = interpolator(t_new)
    
    # Second FFT
    X = np.fft.fft(x)
    
    # Calculate amplitudes
    fast_extract_amp = np.abs(X)
    
    # Get DC component
    dc = fast_extract_amp[0]
    
    # Fold and scale the amplitudes
    n_harmonics = len(x)//2 // num_bins
    indices = np.arange(1, n_harmonics + 1) * num_bins
    Amp = fast_extract_amp[indices] * 2 / len(x)
    
    # Calculate phase
    phi = np.angle(X[indices])
    
    return f, Amp, phi, dc