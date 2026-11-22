from fastapi import FastAPI
import tensorflow as tf
import joblib
import pandas as pd

app = FastAPI(title="Predicción de Lluvias en Australia")

# Cargar artefactos y modelo al iniciar
artefactos = joblib.load("preprocesador.joblib")
imputer = artefactos["imputer"]
scaler = artefactos["scaler"]
continuas = artefactos["continuas"]
columnas_modelo = artefactos["columnas_modelo"]

modelo = tf.keras.models.load_model("modelo_lluvia_australia_tuned.keras")

@app.post("/predict")
def predecir_lluvia(datos: dict):
    # Convertir entrada a DataFrame y asegurar el orden exacto de las 34 columnas
    df_entrada = pd.DataFrame([datos])
    df_entrada = df_entrada.reindex(columns=columnas_modelo, fill_value=0)
    
    # Aplicar imputación y estandarización sobre las variables continuas
    df_entrada[continuas] = scaler.transform(imputer.transform(df_entrada[continuas]))
    
    # Inferencia con Keras
    X_final = df_entrada.astype("float32").values
    probabilidad = float(modelo.predict(X_final, verbose=0)[0][0])
    
    # Si optimizaron el threshold en el notebook (ej. 0.35), reemplaza 0.5 por ese valor
    umbral = 0.5
    prediccion = "Yes" if probabilidad >= umbral else "No"
    
    return {
        "RainTomorrow": prediccion,
        "probabilidad_lluvia": round(probabilidad, 4)
    }