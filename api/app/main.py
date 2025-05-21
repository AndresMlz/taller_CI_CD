# main.py
from fastapi import FastAPI
import joblib
import numpy as np
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response
 
app = FastAPI()
 
# Cargar el modelo entrenado
model = joblib.load("app/model.pkl")
 
# Métrica Prometheus
predict_counter = Counter("predict_requests_total", "Número total de predicciones")
 
@app.get("/")
def read_root():
    return {"message": "API de predicción está funcionando"}
 
@app.get("/predict")
def predict(x1: float, x2: float, x3: float, x4: float):
    predict_counter.inc()  # Incrementar la métrica
    data = np.array([[x1, x2, x3, x4]])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}
 
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")