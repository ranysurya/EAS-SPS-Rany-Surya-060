import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk mensimulasikan sinyal sensor
def generate_sensor_signal(sensor, t):
    if sensor == "Accelerometer":
        acc_x = np.sin(2 * np.pi * 10 * t)  # Sinyal akselerasi sumbu x
        acc_y = np.sin(2 * np.pi * 15 * t)  # Sinyal akselerasi sumbu y
        acc_z = np.cos(2 * np.pi * 5 * t)   # Sinyal akselerasi sumbu z
        sensor_signal = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
    elif sensor == "Load Cell":
        # Simulasi gaya (N)
        force = 1000 * np.abs(np.sin(2 * np.pi * 2 * t))  # Gaya bervariasi secara sinusoidal
        # Menghitung strain dan tegangan keluaran
        strain = force / (200e9 * 0.001)  # Modulus elastisitas dan luas penampang
        sensor_signal = 2.0 * strain  # Tegangan keluaran (Volt)
    elif sensor == "Ultrasonik":
        # Simulasi waktu tempuh gelombang ultrasonik
        time_of_flight = 0.005 + 0.001 * np.sin(2 * np.pi * 1 * t)  # Waktu tempuh bervariasi
        sensor_signal = (343 * time_of_flight) / 2  # Menghitung jarak
    elif sensor == "Kinect":
        disparity = 50 + 20 * np.sin(2 * np.pi * 0.5 * t)
        Z = (500 * 0.075) / disparity
        sensor_signal = Z  # Kedalaman sebagai sinyal
    elif sensor == "Voice Recognition":
        sensor_signal = (np.sin(2 * np.pi * 1 * t) > 0).astype(float)  # Sinyal suara biner
    else:
        sensor_signal = np.zeros_like(t)
    return sensor_signal

# Parameter umum
duration = 1  # Durasi dalam detik
sampling_rate = 1000  # Frekuensi sampling dalam Hz
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Sensor data
accelerometer_signal = generate_sensor_signal("Accelerometer", t)
load_cell_signal = generate_sensor_signal("Load Cell", t)
ultrasonic_signal = generate_sensor_signal("Ultrasonik", t)
kinect_signal = generate_sensor_signal("Kinect", t)
voice_recognition_signal = generate_sensor_signal("Voice Recognition", t)

# Plotting semua sinyal
plt.figure(figsize=(12, 10))

# Akselerometer
plt.subplot(5, 1, 1)
plt.plot(t, accelerometer_signal, label="Accelerometer Signal", color="g")
plt.title("Accelerometer Sensor")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

# Load Cell
plt.subplot(5, 1, 2)
plt.plot(t, load_cell_signal, label="Load Cell Signal", color="m")
plt.title("Load Cell Sensor")
plt.ylabel("Voltage (V)")
plt.grid()
plt.legend()

# Ultrasonik
plt.subplot(5, 1, 3)
plt.plot(t, ultrasonic_signal, label="Ultrasonik Signal", color="r")
plt.title("Ultrasonik Sensor")
plt.ylabel("Distance (m)")
plt.grid()
plt.legend()

# Kinect
plt.subplot(5, 1, 4)
plt.plot(t, kinect_signal, label="Kinect Depth Signal", color="b")
plt.title("Kinect Sensor")
plt.ylabel("Depth (m)")
plt.grid()
plt.legend()

# Voice Recognition
plt.subplot(5, 1, 5)
plt.plot(t, voice_recognition_signal, label="Voice Recognition Signal", color="c")
plt.title("Voice Recognition Sensor")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.tight_layout()
plt.xlabel("Time (s)")
plt.show()
