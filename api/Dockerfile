# Imagen base ligera de Python
FROM python:3.10-slim
 
# Directorio de trabajo dentro del contenedor
WORKDIR /app
 
# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copiar el código de la app
COPY app/ app/
 
# Exponer el puerto (opcional)
EXPOSE 80
 
# Comando para lanzar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]