import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Global variables
sensor_signal = None
noise_signal = None
result_signal = None
dft_result = None
dft_accelerometer = None
t = None

def generate_signals():
    global sensor_signal, noise_signal, result_signal, dft_result, dft_accelerometer, t

    # Generate time vector
    t = np.linspace(0, 2, 1000)

    # Rumus percepatan akselerometer
    acc_x = np.sin(2 * np.pi * 2 * t)  # Contoh untuk sumbu x
    acc_y = np.sin(2 * np.pi * 8 * t)  # Contoh untuk sumbu y
    acc_z = np.cos(2 * np.pi * 10 * t)  # Contoh untuk sumbu z

    # Generate sensor specific signal
    sensor = selected_sensor.get()
    if sensor == "Accelerometer":
        sensor_signal = (np.sqrt(acc_x**2 + acc_y**2 + acc_z**2))
        dft_accelerometer = np.abs(np.fft.fft(sensor_signal))[:500]  # DFT khusus akselerometer
    elif sensor == "Load Cell":
        force = 1000 * np.abs(np.sin(2 * np.pi * 2 * t))  # Gaya bervariasi secara sinusoidal
        strain = force / (200e9 * 0.001)  # Modulus elastisitas dan luas penampang
        sensor_signal = 2.0 * strain  # Tegangan keluaran (Volt)
    elif sensor == "Ultrasonik":
        time_of_flight = 0.005 + 0.001 * np.sin(2 * np.pi * 1 * t)
        sensor_signal = (343 * time_of_flight) / 2  # Menghitung jarak
    elif sensor == "Kinect":
        disparity = 50 + 20 * np.sin(2 * np.pi * 0.5 * t)
        Z = (500 * 0.075) / disparity
        sensor_signal = Z  # Kedalaman sebagai sinyal
    elif sensor == "Voice Recognition":
        sensor_signal = (np.sin(2 * np.pi * 1 * t) > 0).astype(float)
    else:
        sensor_signal = np.zeros_like(t)

    # Generate noise signal (sine wave with noise frequency)
    noise_amp = noise_amplitude.get()
    noise_freq = noise_frequency.get()
    noise_signal = noise_amp * np.sin(2 * np.pi * noise_freq * t)

    # Perform selected operation
    operation = signal_operation.get()
    if operation == "Add":
        result_signal = sensor_signal + noise_signal
    elif operation == "Multiply":
        result_signal = sensor_signal * noise_signal
    elif operation == "Convolve":
        result_signal = np.convolve(sensor_signal, noise_signal, mode='same')
    elif operation == "Calculate DFT":
        result_signal = sensor_signal

    # Perform DFT on result signal
    dft_result = np.abs(np.fft.fft(result_signal))[:500]
    update_plots()

def update_plots():
    # Clear previous plots
    for ax in axes:
        ax.clear()

    # Check if signals are empty (reset state)
    if sensor_signal is None or noise_signal is None or result_signal is None:
        canvas.draw()
        return

    # Plot sensor-specific signal
    axes[0].plot(t, sensor_signal, color='#FF6F61')
    axes[0].set_title(f"{selected_sensor.get()} Signal", color="#6D6875")
    axes[0].set_xlabel("Time [s]", color="#6D6875")
    axes[0].set_ylabel("Amplitude [V]", color="#6D6875")

    # Plot noise signal
    axes[1].plot(t, noise_signal, color='#A5A58D')
    axes[1].set_title("Noise Signal", color="#6D6875")
    axes[1].set_xlabel("Time [s]", color="#6D6875")
    axes[1].set_ylabel("Amplitude [V]", color="#6D6875")

    # Plot result signal
    axes[2].plot(t, result_signal[:len(t)], color='#55A630')
    axes[2].set_title(f"Result of {signal_operation.get()}", color="#6D6875")
    axes[2].set_xlabel("Time [s]", color="#6D6875")
    axes[2].set_ylabel("Amplitude [V]", color="#6D6875")

    # Plot DFT result
    freqs = np.linspace(0, 500, len(dft_result))
    if selected_sensor.get() == "Accelerometer":
        axes[3].stem(freqs, dft_accelerometer, linefmt='#0077B6', markerfmt='o', basefmt=" ")
        axes[3].set_title("DFT of Accelerometer Signal", color="#6D6875")
    else:
        axes[3].stem(freqs, dft_result, linefmt='#0077B6', markerfmt='o', basefmt=" ")
        axes[3].set_title("DFT Result", color="#6D6875")

    axes[3].set_xlabel("Frequency [Hz]", color="#6D6875")
    axes[3].set_ylabel("Amplitude", color="#6D6875")

    # Set plot background color to lilac
    for ax in axes:
        ax.set_facecolor('#E6C9FF')  # Lilac background color

    # Adjust subplot spacing
    fig.tight_layout(pad=3.0)

    canvas.draw()

def update_noise_labels():
    amp_label.config(text=f"Amplitude: {noise_amplitude.get():.2f}")
    freq_label.config(text=f"Frequency: {noise_frequency.get():.2f} Hz")

def reset():
    global sensor_signal, noise_signal, result_signal, dft_result, dft_accelerometer, t

    sensor_signal = None
    noise_signal = None
    result_signal = None
    dft_result = None
    dft_accelerometer = None
    t = None

    noise_amplitude.set(1.0)
    noise_frequency.set(5.0)
    signal_operation.set("Add")
    selected_sensor.set("Accelerometer")

    update_noise_labels()
    update_plots()

# GUI Setup
root = tk.Tk()
root.title("Interactive Signal Visualization")
root.geometry("1200x800")
root.configure(bg="#fcd4f8")

# Frames
controls_frame = ttk.Frame(root, padding="10")
controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
plot_frame = ttk.Frame(root, padding="10")
plot_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

style = ttk.Style()
style.configure("TFrame", background="#F4E7E7")
style.configure("TLabel", background="#F4E7E7", foreground="#6D6875", font=("Arial", 10))
style.configure("TButton", background="#FFADAD", foreground="#6D6875")
style.configure("TCombobox", background="#FFCAD4", foreground="#6D6875")

# Add system information label
info_label = ttk.Label(controls_frame, text="SISTEM PENGOLAHAN SINYAL\nNama: Rany Surya Oktavia\nNRP: 2042231060", font=("Times New Roman", 12, "bold"))
info_label.pack(pady=10)

# Sensor Selection
ttk.Label(controls_frame, text="Select Sensor:").pack(pady=5)
selected_sensor = tk.StringVar(value="Accelerometer")
sensor_menu = ttk.Combobox(controls_frame, textvariable=selected_sensor, state="readonly")
sensor_menu['values'] = ("Accelerometer", "Load Cell", "Ultrasonik", "Kinect", "Voice Recognition")
sensor_menu.pack(fill=tk.X, padx=5)
sensor_menu.bind("<<ComboboxSelected>>", lambda e: generate_signals())

# Noise Amplitude Control
ttk.Label(controls_frame, text="Noise Amplitude:").pack(pady=5)
noise_amplitude = tk.DoubleVar(value=1.0)
amp_slider = ttk.Scale(controls_frame, from_=0.1, to=5.0, variable=noise_amplitude, command=lambda e: [generate_signals(), update_noise_labels()])
amp_slider.pack(fill=tk.X, padx=5)
amp_label = ttk.Label(controls_frame, text=f"Amplitude: {noise_amplitude.get():.2f}")
amp_label.pack(pady=2)

# Noise Frequency Control
ttk.Label(controls_frame, text="Noise Frequency (Hz):").pack(pady=5)
noise_frequency = tk.DoubleVar(value=5.0)
freq_slider = ttk.Scale(controls_frame, from_=1.0, to=50.0, variable=noise_frequency, command=lambda e: [generate_signals(), update_noise_labels()])
freq_slider.pack(fill=tk.X, padx=5)
freq_label = ttk.Label(controls_frame, text=f"Frequency: {noise_frequency.get():.2f} Hz")
freq_label.pack(pady=2)

# Signal Operation Selection
ttk.Label(controls_frame, text="Signal Operation:").pack(pady=5)
signal_operation = tk.StringVar(value="Add")
operation_menu = ttk.Combobox(controls_frame, textvariable=signal_operation, state="readonly")
operation_menu['values'] = ("Add", "Multiply", "Convolve", "Calculate DFT")
operation_menu.pack(fill=tk.X, padx=5)
operation_menu.bind("<<ComboboxSelected>>", lambda e: generate_signals())

# Buttons
ttk.Button(controls_frame, text="Reset", command=reset).pack(pady=20, fill=tk.X)

# Plot Setup
fig = Figure(figsize=(9, 7), dpi=100)
axes = [fig.add_subplot(2, 2, i+1) for i in range(4)]
canvas = FigureCanvasTkAgg(fig, plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Generate initial signals
t = np.linspace(0, 2, 1000)
sound_signal = None
noise_signal = None
result_signal = None
dft_result = None
update_plots()

# Run GUI
root.mainloop()
