import json
import boto3

client = boto3.client('lambda')

def filtro_pasa_bajos(coeficientes, frecuencias, fs, N, fc):
    return [(0, 0) if abs(f) > fc else c for c, f in zip(coeficientes, frecuencias)]

def filtro_pasa_altos(coeficientes, frecuencias, fs, N, fc):
    return [(0, 0) if abs(f) < fc else c for c, f in zip(coeficientes, frecuencias)]

def filtro_pasa_banda(coeficientes, frecuencias, fs, N, f1, f2):
    return [(0, 0) if not (f1 <= abs(f) <= f2) else c for c, f in zip(coeficientes, frecuencias)]

def filtro_rechaza_banda(coeficientes, frecuencias, fs, N, f1, f2):
    return [(0, 0) if f1 <= abs(f) <= f2 else c for c, f in zip(coeficientes, frecuencias)]

def aplicar_filtro(coeficientes, frecuencias, fs, N, filtro, parametros):
    if filtro == "pasa_bajos":
        return filtro_pasa_bajos(coeficientes, frecuencias, fs, N, parametros["fc"])
    elif filtro == "pasa_altos":
        return filtro_pasa_altos(coeficientes, frecuencias, fs, N, parametros["fc"])
    elif filtro == "pasa_banda":
        return filtro_pasa_banda(coeficientes, frecuencias, fs, N, parametros["f1"], parametros["f2"])
    elif filtro == "rechaza_banda":
        return filtro_rechaza_banda(coeficientes, frecuencias, fs, N, parametros["f1"], parametros["f2"])
    else:
        return coeficientes

def lambda_handler(event, context):
    coeficientes = event["coeficientes"]
    frecuencias = event["frecuencias"]
    fs = event["fs"]
    filtro_tipo = event["filtro"]
    parametros_filtro = event["parametros"]

    N = len(coeficientes)

    coef_filtrados = aplicar_filtro(coeficientes, frecuencias, fs, N, filtro_tipo, parametros_filtro)

    return {
        "coef_filtrados": coef_filtrados
    }
