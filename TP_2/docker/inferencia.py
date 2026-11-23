import os
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Predicción de Lluvias en Australia")

# --- Configuración de Rutas con os.path ---
RUTA_BASE = os.getcwd()
RUTA_PREPROCESADOR = os.path.join(RUTA_BASE, "preprocesador.joblib")
RUTA_MODELO = os.path.join(RUTA_BASE, "modelo_lluvia_australia_tuned.keras")
RUTA_COORDENADAS = os.path.join(RUTA_BASE, "locations_with_coordinates.csv")

# Cargar artefactos y modelo al iniciar de forma robusta
if not os.path.exists(RUTA_PREPROCESADOR):
    raise FileNotFoundError(f"No se encontró el archivo del preprocesador en {RUTA_PREPROCESADOR}")
if not os.path.exists(RUTA_MODELO):
    raise FileNotFoundError(f"No se encontró el modelo Keras en {RUTA_MODELO}")

artefactos = joblib.load(RUTA_PREPROCESADOR)
imputer = artefactos["imputer"]
scaler = artefactos["scaler"]
continuas = artefactos["continuas"]
columnas_modelo = artefactos["columnas_modelo"]

modelo = tf.keras.models.load_model(RUTA_MODELO)

# Diccionario para mapeo cardinal de vientos (16 direcciones)
direcciones_viento = ["E", "ENE", "NE", "NNE", "N", "NNW", "NW", "WNW", "W", "WSW", "SW", "SSW", "S", "SSE", "SE", "ESE"]
mapeo_viento = {dir_texto: i for i, dir_texto in enumerate(direcciones_viento)}

def preprocesar_nuevos_datos(df_nuevo, prep, ruta_coordenadas=RUTA_COORDENADAS):
    """Preprocesa un DataFrame de nuevas observaciones aplicando las mismas transformaciones del entrenamiento."""
    df = df_nuevo.copy()

    # 1. Tratamiento de Fechas y Estacionalidad
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["Mes_sin"] = np.sin(2 * np.pi * df["Month"] / 12)
    df["Mes_cos"] = np.cos(2 * np.pi * df["Month"] / 12)

    # 2. Incorporación de Coordenadas Geográficas (Latitud, Longitud)
    if os.path.exists(ruta_coordenadas):
        loc_coords = pd.read_csv(ruta_coordenadas)
        df = pd.merge(df, loc_coords, on="Location", how="left")
    else:
        # Fallbacks seguros aproximados de Sídney si no se encuentra el csv
        df["Latitud"] = df.get("Latitud", -33.8688)
        df["Longitud"] = df.get("Longitud", 151.2093)

    # 3. Indicadoras de Faltantes (antes de imputar)
    faltante_alto = ["Evaporation", "Sunshine", "Cloud9am", "Cloud3pm"]
    for c in faltante_alto:
        df[f"{c}_faltante"] = df[c].isna().astype(int)

    # 4. Transformaciones logarítmicas de variables asimétricas
    df["RainToday"] = (df["RainToday"] == "Yes").astype(int)
    df["Rainfall"] = np.log1p(df["Rainfall"])
    df["Evaporation"] = np.log1p(df["Evaporation"])

    # 5. Codificación Cíclica de Direcciones de Viento
    cols_viento = ["WindGustDir", "WindDir9am", "WindDir3pm"]
    for col in cols_viento:
        df[f"{col}_faltante"] = df[col].isna().astype(int)
        df[col] = df[col].ffill().fillna("E")
        df[f"{col}_idx"] = df[col].map(mapeo_viento)
        df[f"{col}_sin"] = np.sin(2 * np.pi * df[f"{col}_idx"] / 16).fillna(0)
        df[f"{col}_cos"] = np.cos(2 * np.pi * df[f"{col}_idx"] / 16).fillna(0)

    # Reindexar columnas al esquema estricto del modelo original (llenando dummies/faltantes vacías con 0)
    df = df.reindex(columns=columnas_modelo, fill_value=0)

    # 6. Imputación y Escalado de Variables Continuas
    df[continuas] = scaler.transform(imputer.transform(df[continuas]))
    return df

@app.post("/predict")
def predecir_lluvia(datos: dict):
    try:
        # Convertir JSON de entrada a DataFrame
        df_entrada = pd.DataFrame([datos])
        
        # Aplicar el pipeline de preprocesamiento completo
        df_procesado = preprocesar_nuevos_datos(df_entrada, artefactos, RUTA_COORDENADAS)
        
        # Convertir a arreglo numpy para TensorFlow
        X_final = df_procesado.astype("float32").values
        
        # Obtener predicción de probabilidad continua
        probabilidad = float(modelo.predict(X_final, verbose=0)[0][0])

        # Aplicar el umbral óptimo de decisión calibrado
        umbral_optimo = 0.6001
        prediccion = "Yes" if probabilidad >= umbral_optimo else "No"

        return {
            "RainTomorrow": prediccion,
            "probabilidad_lluvia": round(probabilidad, 4),
            "threshold_applied": umbral_optimo
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la solicitud: {str(e)}")