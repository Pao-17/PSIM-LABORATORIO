import json
import math

def carga_signal_json(json_string):
    data = json.loads(json_string)
    # Aseguramos que los valores de la señal sean flotantes
    return [float(value) for value in data["signal"].split(",")]

def Transformada_discreta_directa(signal):
    N = len(signal)
    coeficientes = []  
    magnitudft = []
    for k in range(N):
        real = sum(signal[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        imag = sum(signal[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        coeficientes.append((real, imag))  # Guardamos los coeficientes complejos de fourier en la lista
        magnitude = math.sqrt(real**2 + imag**2)  # Calculamos la magnitud de la frecuencia utulizando los coeficientes
        magnitudft.append(magnitude) # Guardamos las magnitudes calculadas en la lista
    return coeficientes, magnitudft

def Transformada_inversa(coeficientes):
   #Hacemos la sumatoria con los coeficientes calculados en la funcion de transformada directa
    N = len(coeficientes)
    reconstruccion = []
    for n in range(N):
        sum_real = sum(coeff[0] * math.cos(2 * math.pi * k * n / N) - coeff[1] * math.sin(2 * math.pi * k * n / N) for k, coeff in enumerate(coefficients))
        reconstruccion.append(sum_real / N)  # Dividir por N para la normalización
    return reconstruccion

def lambda_handler(event, context):
    json_string = event["json_string"]
    
    signal = carga_signal_json(json_string)
    coeficientes, magnitud = Transformada_discreta_directa(signal)
    reconstruccion = Transformada_inversa(coeficientes)  
    return {
        "MAGNITUD": magnitud,
        "COEFICIENTES": coeficientes,
        "RECONSTRUCCIÓN": reconstruccion  # Señal reconstruida
        #"signal": signal

    }


