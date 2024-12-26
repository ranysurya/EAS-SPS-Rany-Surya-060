import numpy as np

# Fungsi untuk mensimulasikan sinyal suara dari mikrofon
def voice_signal(frequency, sampling_rate, duration, amplitude):
    # Membuat vektor waktu
    t = np.linspace(0, duration, int(sampling_rate * duration))
    # Sinyal sinusoidal suara
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    return t, signal

# Fungsi untuk mensimulasikan input keypad (digital signal)
def keypad_input(sampling_rate, duration, min_voltage, max_voltage):
    # Membuat vektor waktu
    t = np.linspace(0, duration, int(sampling_rate * duration))
    # Mensimulasikan sinyal digital (misalnya tombol ditekan dengan durasi tertentu)
    signal = np.zeros_like(t)
    pressed_duration = duration / 4  # Waktu tombol ditekan (25% durasi)
    signal[t < pressed_duration] = max_voltage
    signal[t >= pressed_duration] = min_voltage
    return t, signal

# Parameter sinyal suara (mikrofon)
voice_frequency = 440  # Frekuensi suara (Hz)
sampling_rate = 1000  # Laju sampling (samples per second)
duration = 1  # Durasi sinyal (detik)
voice_amplitude = 1  # Amplitudo maksimum sinyal suara

# Parameter sinyal keypad (digital)
min_voltage = 0  # Level tegangan minimum
max_voltage = 5  # Level tegangan maksimum

# Menghasilkan sinyal
t_voice, voice = voice_signal(voice_frequency, sampling_rate, duration, voice_amplitude)
t_keypad, keypad = keypad_input(sampling_rate, duration, min_voltage, max_voltage)

# Menggabungkan sinyal suara dan sinyal keypad
combined_signal = voice + keypad

# Output sampel untuk pemeriksaan
print("Voice Signal (First 10 Samples):", voice[:10])
print("Keypad Signal (First 10 Samples):", keypad[:10])
print("Combined Signal (First 10 Samples):", combined_signal[:10])
