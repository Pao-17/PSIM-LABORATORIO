import json
import math

def load_signal_from_json(json_string):
    data = json.loads(json_string)
    # Aseguramos que los valores de la señal sean flotantes
    return [float(value) for value in data["signal"].split(",")]

def Direct_transform(signal):
    N = len(signal)
    coefficients = []  
    dft_result = []
    for k in range(N):
        real = sum(signal[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        imag = sum(signal[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        coefficients.append((real, imag))  # Guardamos los coeficientes complejos de fourier en la lista
        magnitude = math.sqrt(real**2 + imag**2)  # Calculamos la magnitud de la frecuencia utulizando los coeficientes
        dft_result.append(magnitude) # Guardamos las magnitudes calculadas en la lista
    return coefficients, dft_result

def inverse_transform(coefficients):
    N = len(coefficients)
    reconstructed_signal = []
    for n in range(N):
        sum_real = sum(coeff[0] * math.cos(2 * math.pi * k * n / N) - coeff[1] * math.sin(2 * math.pi * k * n / N) for k, coeff in enumerate(coefficients))
        reconstructed_signal.append(sum_real / N)  # Dividir por N para la normalización
    return reconstructed_signal

def lambda_handler(event, context):
    json_string = event["json_string"]
    
    signal = load_signal_from_json(json_string)
    #coefficients, dft_magnitude = Direct_transform(signal)
    #reconstructed_signal = inverse_transform(coefficients)  
    return {
        "dft_magnitude": dft_magnitude,
        "coeficientes": coefficients,
        "reconstructed_signal": reconstructed_signal  # Señal reconstruida

    }
