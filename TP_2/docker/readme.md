# API de Predicción de Lluvias en Australia

Servicio RESTful desarrollado con **FastAPI** y **TensorFlow** para predecir la probabilidad de precipitaciones al día siguiente (*RainTomorrow*) a partir de variables meteorológicas históricas y actuales.

> **Contexto Académico:** Proyecto presentado para la cátedra de *Aprendizaje Automático 1* — *UNR*.

## Arquitectura y Ambiente

El proyecto está completamente contenerizado para garantizar la reproducibilidad del entorno de ejecución sin conflictos de dependencias.

* **Lenguaje:** Python `3.12` (imagen base `python:3.12-slim`).
* **Framework Web:** FastAPI `0.115.0` + Uvicorn `0.30.6`.
* **Machine Learning & Procesamiento:** TensorFlow CPU `2.21.0`, Scikit-Learn `1.9.1`, Pandas y NumPy.
* **Artefactos del Modelo:**
  * `inferencia.py`: Lógica de la API y definición de endpoints.
  * `preprocesador.joblib`: Pipeline de transformación y escalado de variables.
  * `modelo_lluvia_australia_tuned.keras`: Red neuronal entrenada y ajustada.

## Despliegue con Docker

Asegúrate de tener **Docker** instalado y en ejecución en tu sistema, y de encontrarte en el directorio raíz del proyecto (donde reside el `Dockerfile`).

### 1. Construcción de la imagen

Compila la imagen localmente asignándole la etiqueta `lluvia-australia-nn`:

```bash
docker build -t lluvia-australia-nn .
```

### 2. Ejecución del contenedor

Inicia el servicio en segundo plano (`-d`), mapeando el puerto `8000` de tu máquina local al puerto `8000` expuesto por el contenedor:

```bash
docker run --rm -d -p 8000:8000 --name api-lluvia lluvia-australia-nn
```

*(Opcional)* Para verificar que el servidor levantó correctamente y revisar los registros de TensorFlow/Uvicorn:

```bash
docker logs api-lluvia
```

### 3. Reinicio o actualización del entorno

Si realizas cambios en el código o necesitas reconstruir el contenedor desde cero:

```bash
docker rm -f api-lluvia
docker build -t lluvia-australia-nn .
docker run --rm -d -p 8000:8000 --name api-lluvia lluvia-australia-nn
```

## Guía de Uso y Pruebas

Una vez activo el contenedor, puedes interactuar con la documentación automática (Swagger UI) desde tu navegador:

 [**http://localhost:8000/docs**](http://localhost:8000/docs)

### Pasos para ejecutar una predicción de prueba:

1. En la interfaz web bajo el título **Predicción de Lluvias en Australia**, ubica el endpoint **`POST /predict`** (barra verde) y haz clic para desplegarlo.
2. Presiona el botón **`Try it out`** (esquina superior derecha del panel).
3. En el campo **Request body**, reemplaza el esquema por defecto con alguno de los siguientes casos de prueba en formato JSON:

#### Caso A: Escenario con alta probabilidad de lluvia

```json
{
  "Date": "2026-10-10",
  "Location": "Sydney",
  "MinTemp": 16.5,
  "MaxTemp": 20.2,
  "Rainfall": 18.4,
  "Evaporation": 2.0,
  "Sunshine": 0.5,
  "WindGustDir": "S",
  "WindGustSpeed": 65.0,
  "WindDir9am": "SE",
  "WindDir3pm": "SE",
  "WindSpeed9am": 24.0,
  "WindSpeed3pm": 30.0,
  "Humidity9am": 82.0,
  "Humidity3pm": 89.0,
  "Pressure9am": 1004.2,
  "Pressure3pm": 1001.5,
  "Cloud9am": 8.0,
  "Cloud3pm": 8.0,
  "Temp9am": 17.8,
  "Temp3pm": 18.5,
  "RainToday": "No"
}
```

#### Caso B: Escenario despejado (sin lluvia)

```json
{
  "Date": "2026-10-10",
  "Location": "Sydney",
  "MinTemp": 16.5,
  "MaxTemp": 20.2,
  "Rainfall": 18.4,
  "Evaporation": 2.0,
  "Sunshine": 0.5,
  "WindGustDir": "S",
  "WindGustSpeed": 65.0,
  "WindDir9am": "SE",
  "WindDir3pm": "SE",
  "WindSpeed9am": 24.0,
  "WindSpeed3pm": 30.0,
  "Humidity9am": 12.0,
  "Humidity3pm": 19.0,
  "Pressure9am": 1024.2,
  "Pressure3pm": 1021.5,
  "Cloud9am": 2.0,
  "Cloud3pm": 8.0,
  "Temp9am": 17.8,
  "Temp3pm": 18.5,
  "RainToday": "No"
}
```

4. Haz clic en el botón azul **`Execute`**.
5. Verifica la sección **Responses**: deberías recibir un código de estado **`200 OK`** junto con el JSON de salida que indica la predicción binaria (`"RainTomorrow"`) y su probabilidad asociada (`"probabilidad_lluvia"`).

## Diccionario de Variables de Entrada

| Variable | Tipo | Descripción |
| :--- | :--- | :--- |
| `MinTemp` / `MaxTemp` | `float` | Temperaturas mínima y máxima registradas en el día ($^\circ\text{C}$). |
| `Rainfall` | `float` | Precipitación acumulada en las últimas 24 horas ($\text{mm}$). |
| `Evaporation` / `Sunshine` | `float` | Evaporación ($\text{mm}$) y horas de sol brillante en el día. |
| `WindGustSpeed` | `float` | Velocidad de la ráfaga de viento más fuerte ($\text{km/h}$). |
| `WindSpeed9am` / `3pm` | `float` | Velocidad del viento a las 9:00 y 15:00 hs ($\text{km/h}$). |
| `Humidity9am` / `3pm` | `float` | Humedad relativa a las 9:00 y 15:00 hs ($\%$). |
| `Pressure9am` / `3pm` | `float` | Presión atmosférica reducida al nivel del mar ($\text{hPa}$). |
| `Cloud9am` / `3pm` | `float` | Fracción de cielo cubierto por nubes (escala de octas, $0$ a $8$). |
| `Temp9am` / `3pm` | `float` | Temperatura registrada a las 9:00 y 15:00 hs ($\text{h}^\circ\text{C}$). |
| `RainToday` | `int` | Indicador binario de lluvia hoy (`1` = Sí, `0` = No). |