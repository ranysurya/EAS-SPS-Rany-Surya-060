import numpy as np

# Kecepatan suara di udara (343 m/s pada suhu ruang, dapat disesuaikan)
def sound_speed(temperature=25):
    return 331.4 + 0.606 * temperature  # m/s

# Fungsi untuk menghitung waktu tempuh gelombang ultrasonik berdasarkan jarak
def ultrasonic_time(distance, temperature=25):
    v = sound_speed(temperature)  # Kecepatan suara
    return 2 * distance / v  # Waktu bolak-balik (s)

# Fungsi untuk membuat sinyal ultrasonik
def ultrasonic_signal(distance, frequency, sampling_rate, duration, temperature=25):
    # Waktu simulasi
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    
    # Waktu tempuh ultrasonik
    travel_time = ultrasonic_time(distance, temperature)
    
    # Sinyal ultrasonik sinus (0-5V)
    ultrasonic_wave = 2.5 * (np.sin(2 * np.pi * frequency * t) + 1)
    
    # Memberikan logika delay untuk sinyal pantulan
    echo_wave = np.zeros_like(t)
    echo_start_idx = int(travel_time * sampling_rate)  # Indeks untuk memulai sinyal pantulan
    if echo_start_idx < len(t):
        echo_wave[echo_start_idx:] = ultrasonic_wave[:len(t) - echo_start_idx]
    
    return t, ultrasonic_wave, echo_wave

# Parameter sensor ultrasonik
distance = 2  # Jarak (meter)
frequency = 40 * 10**3  # Frekuensi sinyal ultrasonik (40 kHz)
sampling_rate = 100000  # Sampling rate (100 kHz)
duration = 0.01  # Durasi simulasi (10 ms)
temperature = 25  # Suhu udara (°C)

# Generate sinyal
t, ultrasonic_wave, echo_wave = ultrasonic_signal(distance, frequency, sampling_rate, duration, temperature)

# Output sampel untuk pemeriksaan
print("Time (First 10 Samples):", t[:10])
print("Ultrasonic Wave (First 10 Samples):", ultrasonic_wave[:10])
print("Echo Wave (First 10 Samples):", echo_wave[:10])
