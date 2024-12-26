import numpy as np

# Fungsi untuk menghasilkan sinyal kedalaman berdasarkan intensitas IR
def Depth_signal(frequency, sampling_rate, duration, min_depth, max_depth):
    t = np.linspace(0, duration, int(sampling_rate * duration))
    # Menggunakan sinyal sinusoidal untuk mensimulasikan data kedalaman
    Depth = min_depth + (max_depth - min_depth) * (0.5 * (1 + np.sin(2 * np.pi * frequency * t)))
    return t, Depth

# Fungsi untuk menghasilkan sinyal audio (kombinasi dari dua mikrofon)
def Audio_signal(frequency1, frequency2, sampling_rate, duration, amplitude):
    t = np.linspace(0, duration, int(sampling_rate * duration))
    # Sinyal audio gabungan dari dua sumber
    Audio = amplitude * (np.sin(2 * np.pi * frequency1 * t) + np.sin(2 * np.pi * frequency2 * t)) / 2
    return t, Audio

# Parameter sinyal kedalaman
depth_frequency = 1  # Frekuensi untuk sinyal kedalaman (Hz)
depth_sampling_rate = 100  # Laju sampling (samples per second)
depth_duration = 2  # Durasi (detik)
min_depth = 0.5  # Kedalaman minimum
max_depth = 5  # Kedalaman maksimum

# Parameter sinyal audio
audio_frequency1 = 200  # Frekuensi mikrofon 1 (Hz)
audio_frequency2 = 250  # Frekuensi mikrofon 2 (Hz)
audio_sampling_rate = 1000  # Laju sampling (samples per second)
audio_duration = 0.02  # Durasi (detik)
audio_amplitude = 1  # Amplitudo maksimum

# Menghasilkan sinyal
t_depth, Depth = Depth_signal(depth_frequency, depth_sampling_rate, depth_duration, min_depth, max_depth)
t_audio, Audio = Audio_signal(audio_frequency1, audio_frequency2, audio_sampling_rate, audio_duration, audio_amplitude)

# Output sampel untuk pemeriksaan
print("Depth Signal (First 10 Samples):", Depth[:10])
print("Audio Signal (First 10 Samples):", Audio[:10])
