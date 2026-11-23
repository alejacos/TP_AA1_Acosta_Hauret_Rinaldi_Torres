FROM python:3.12-slim

WORKDIR /app

ENV TF_CPP_MIN_LOG_LEVEL=2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY inferencia.py .
COPY preprocesador.joblib .
COPY modelo_lluvia_australia_tuned.keras .

EXPOSE 8000

CMD ["uvicorn", "inferencia:app", "--host", "0.0.0.0", "--port", "8000"]