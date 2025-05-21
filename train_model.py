# train_model.py
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
 
# Cargar el dataset Iris
X, y = load_iris(return_X_y=True)
 
# Entrenar un modelo
clf = RandomForestClassifier()
clf.fit(X, y)
 
# Guardar el modelo en api/app/
joblib.dump(clf, "api/app/model.pkl")
print("✅ Modelo entrenado y guardado en api/app/model.pkl")