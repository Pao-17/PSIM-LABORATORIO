import json
import math
import boto3

client = boto3.client('lambda')

def generar_tiempo(fs, duracion):
    paso = 1/fs
    num_muestras = math.ceil(duracion / paso)
    tiempo = [i * paso for i in range(num_muestras)]
    return tiempo

def generar_senal(json_string, tiempo):
    data = json.loads(json_string)
    amplitudes = data["amplitud"]
    frecuencias = data["frecuencias"]
    
    senal = [sum(A * math.sin(2 * math.pi * f * t) for A, f in zip(amplitudes, frecuencias)) for t in tiempo]
    return senal

def Transformada_discreta_directa(signal, fs):
    N = len(signal)
    coeficientes = []
    frecuencias = [(k * fs / N) if k < N//2 else ((k - N) * fs / N) for k in range(N)]
    
    for k in range(N):
        real = sum(signal[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        imag = sum(signal[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        coeficientes.append((real, imag))  
    
    return coeficientes, frecuencias

def Transformada_inversa(coeficientes):
    N = len(coeficientes)
    reconstruccion = []
    for n in range(N):
        sum_real = sum(coeff[0] * math.cos(2 * math.pi * k * n / N) - coeff[1] * math.sin(2 * math.pi * k * n / N) for k, coeff in enumerate(coeficientes))
        reconstruccion.append(sum_real / N)
    return reconstruccion

def lambda_handler(event, context):
    print(event)
    body = json.loads(event["body"])
    print(body)

    json_string = body["json_string"]
    filtro_tipo = body["filtro"]
    parametros_filtro = body["parametros"]
    fs = body["fs"]
    duracion = body["duración"]
    
   
    tiempo = generar_tiempo(fs, duracion)
    signal = generar_senal(json_string, tiempo)
    coeficientes, frecuencias = Transformada_discreta_directa(signal, fs)

    
    response = client.invoke(
        FunctionName='FILTROS',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "coeficientes": coeficientes,
            "frecuencias": frecuencias,
            "fs": fs,
            "filtro": filtro_tipo,
            "parametros": parametros_filtro
        })
    )
    
    response_payload = json.load(response['Payload'])

    # Validación de la clave "coef_filtrados"
    if "coef_filtrados" not in response_payload:
        return {"error": "La respuesta de FILTROS no contiene 'coef_filtrados'", "response_payload": response_payload}

    coef_filtrados = response_payload["coef_filtrados"]
    reconstruccion = Transformada_inversa(coef_filtrados)

    return {
        "SIGNAL_ORIGINAL": signal,
        "COEFICIENTES_ORIGINALES": coeficientes,
        "FRECUENCIAS": frecuencias,
        "COEFICIENTES_FILTRADOS": coef_filtrados,
        "SIGNAL_FILTRADA": reconstruccion
    }
