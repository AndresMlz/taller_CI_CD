from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib
import os

# Crear datos de ejemplo
X = np.random.rand(100, 4)
y = np.random.randint(0, 2, 100)

# Entrenar un modelo simple
model = RandomForestClassifier(n_estimators=10)
model.fit(X, y)

# Asegurarnos de que el directorio existe
os.makedirs("app", exist_ok=True)

# Guardar el modelo
joblib.dump(model, "app/model.pkl") 