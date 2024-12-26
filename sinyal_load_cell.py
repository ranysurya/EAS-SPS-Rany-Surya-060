import numpy as np

def load_cell_signal_wave(force_amplitude, frequency, sensitivity, gain, sampling_rate, duration, v_ref=5.0):
    """
    Simulasikan sinyal load cell berbentuk gelombang sinusoidal.
    """
    # Parameter fisik
    spring_constant = 1000  # Konstanta pegas (N/m), sesuaikan dengan load cell yang digunakan

    # Waktu
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    # Gaya sinusoidal (modulasi gaya)
    force = force_amplitude * np.sin(2 * np.pi * frequency * t)  # F(t) = F_ampl * sin(2πft)

    # Regangan mekanis
    strain = force / spring_constant  # ε = F / k

    # Tegangan output load cell
    v_out = sensitivity * strain  # V_out = S * ε

    # Tegangan input HX711 setelah penguatan
    v_adc = gain * v_out  # V_adc = G * V_out

    # Output digital ADC
    n = 24  # Resolusi ADC HX711 (24 bit)
    digital_output = (v_adc / v_ref) * (2 ** n)

    # Batasi nilai digital output ke rentang 0 hingga nilai maksimum ADC
    digital_output = np.clip(digital_output, 0, 2 ** n - 1)

    return t, digital_output


# Contoh penggunaan
force_amplitude = 50  # Amplitudo gaya (N)
frequency = 0.5  # Frekuensi gaya sinusoidal (Hz)
sensitivity = 2e-3 
