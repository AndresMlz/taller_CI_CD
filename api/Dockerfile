# Imagen base ligera de Python
FROM python:3.10-slim
 
# Directorio de trabajo dentro del contenedor
WORKDIR /app
 
# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copiar el código de la app
COPY app/ app/
 
# Generar el modelo durante la construcción
RUN python app/train_model.py

# Exponer el puerto (opcional)
EXPOSE 8000
 
# Comando para lanzar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]