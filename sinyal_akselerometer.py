import numpy as np
from scipy.signal import butter, filtfilt

# Fungsi untuk menghasilkan sinyal akselerometer
def generate_signal(amplitude, frequency, sampling_rate, duration, phase=0):
    # Waktu selama sinyal berlangsung (dalam detik)
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    # Persamaan sinyal dasar
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return t, signal

# Fungsi penguat (Gain)
def apply_gain(signal, gain):
    return gain * signal

# Fungsi switching
def apply_switch(signal, switch_signal):
    return signal * switch_signal

# Fungsi Low-Pass Filter (LPF) sederhana
def apply_lpf(signal, cutoff_frequency, sampling_rate):
    # Parameter filter Butterworth
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(1, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal

# Parameter sinyal
amplitude = 5
frequency = 2  # in Hz
sampling_rate = 100  # in samples per second
duration = 5  # duration in seconds
gain = 3  # Gain (G)
cutoff_frequency = 1.5  # Cutoff frequency for LPF
switch_signal = np.tile([1, 0], int(sampling_rate * duration / 2))[:int(sampling_rate * duration)]  # Sinyal switching (0/1)

# Langkah 1: Generate sinyal akselerometer
t, akselerometer = generate_signal(amplitude, frequency, sampling_rate, duration)

# Langkah 2: Terapkan penguatan
amplified_signal = apply_gain(akselerometer, gain)

# Langkah 3: Terapkan switching
switched_signal = apply_switch(amplified_signal, switch_signal)

# Langkah 4: Terapkan Low-Pass Filter (LPF)
filtered_signal = apply_lpf(switched_signal, cutoff_frequency, sampling_rate)

# Output data untuk pemeriksaan
print("Original Signal (First 10 Samples):", akselerometer[:10])
print("Amplified Signal (First 10 Samples):", amplified_signal[:10])
print("Switched Signal (First 10 Samples):", switched_signal[:10])
print("Filtered Signal (First 10 Samples):", filtered_signal[:10])
