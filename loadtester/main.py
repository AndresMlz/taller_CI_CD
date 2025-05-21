import requests

import random

import time
 
API_URL = "http://api:80/predict"
 
while True:

    # Generar 4 valores aleatorios como entradas

    params = {

        "x1": random.uniform(4.0, 8.0),

        "x2": random.uniform(2.0, 4.5),

        "x3": random.uniform(1.0, 7.0),

        "x4": random.uniform(0.1, 2.5)

    }
 
    try:

        r = requests.get(API_URL, params=params)

        print(f"Input: {params} → Output: {r.json()}")

    except Exception as e:

        print("Error al enviar petición:", e)
 
    time.sleep(1)

 