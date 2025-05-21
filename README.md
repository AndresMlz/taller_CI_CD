
# Taller CI/CD y GitOps para Despliegue de API de IA

Este proyecto implementa una arquitectura de CI/CD con enfoque GitOps utilizando Docker, Kubernetes, GitHub Actions y Argo CD para desplegar una API basada en un modelo de inteligencia artificial. Además, se incluye observabilidad mediante Prometheus y Grafana, así como generación de carga automática para simular tráfico.

---

## Objetivos del Proyecto

- Entrenar y versionar un modelo de machine learning.
- Desplegar una API (FastAPI) que use dicho modelo para hacer inferencia.
- Automatizar el ciclo CI/CD con GitHub Actions.
- Orquestar los recursos con Kubernetes.
- Sincronizar cambios desde GitHub al clúster con Argo CD.
- Monitorear el sistema con Prometheus y Grafana.

---

## Estructura del Proyecto

```
taller_CI_CD/
├── .github/workflows/ci-cd.yml         # Pipeline CI/CD con GitHub Actions
├── api/
│   ├── app/
│   │   ├── main.py                     # API FastAPI con endpoints /predict y /metrics
│   │   └── model.pkl                   # Modelo entrenado
│   ├── Dockerfile
│   └── requirements.txt
├── loadtester/
│   ├── main.py                         # Script que genera peticiones aleatorias a /predict
│   ├── Dockerfile
│   └── requirements.txt
├── train_model.py                      # Script para entrenar y guardar el modelo
├── manifests/                          # Manifiestos Kubernetes
│   ├── api-deployment.yaml
│   ├── loadtester-deployment.yaml
│   ├── prometheus-deployment.yaml
│   ├── grafana-deployment.yaml
│   ├── prometheus.yml
│   ├── grafana-config/
│   │   └── datasources.yaml
│   └── kustomization.yaml
├── argo-cd/
│   ├── app.yaml                        # Definición GitOps de la aplicación para Argo CD
│   └── crd-application.yaml            # CRD para Argo CD (si se instala manualmente)
```

---

## Descripción de Componentes

### 1. Modelo de IA
- Se utiliza el dataset de Iris desde `scikit-learn`.
- El modelo es un clasificador `RandomForestClassifier`.
- Se guarda como `model.pkl` con `joblib`.

### 2. API con FastAPI
- Expuesto en `/predict`: acepta 4 valores `x1` a `x4` y retorna la predicción.
- Expuesto en `/metrics`: expone la métrica `predict_requests_total` para Prometheus.

### 3. LoadTester
- Envia peticiones cada segundo a `/predict` con datos aleatorios.
- Se ejecuta como pod independiente en Kubernetes.

### 4. Docker y GitHub Actions
- La acción `ci-cd.yml` hace lo siguiente:
  - Ejecuta `train_model.py` para regenerar el modelo.
  - Construye las imágenes `api` y `loadtester`.
  - Publica las imágenes en GitHub Container Registry (GHCR).

### 5. Kubernetes y Argo CD
- Todos los recursos se despliegan en Kubernetes mediante manifiestos YAML.
- Se usa `kustomization.yaml` para orquestar despliegue múltiple.
- Argo CD detecta cambios en el repo y sincroniza el estado del clúster automáticamente.

### 6. Observabilidad
- **Prometheus**: scrapea `/metrics` de la API y recolecta `predict_requests_total`.
- **Grafana**: permite visualizar el conteo de predicciones. (pendiente por validar completamente)

---

## Flujo de Trabajo CI/CD

1. El desarrollador hace `git push` a la rama `main`.
2. GitHub Actions ejecuta el workflow:
   - Entrena el modelo
   - Construye imágenes Docker
   - Publica imágenes en GHCR
3. Argo CD detecta el cambio en manifiestos o etiquetas
4. Argo CD sincroniza automáticamente el estado del clúster
5. Kubernetes crea/actualiza los pods: API, LoadTester, Prometheus, Grafana
6. LoadTester genera peticiones que activan el endpoint `/predict`
7. Prometheus recoge las métricas de uso y Grafana puede mostrarlas

---

## Consideraciones finales

- El sistema está funcionando como arquitectura base.
- Aún se está resolviendo un problema con la visualización de métricas.
- El sistema puede ser escalado, versionado o adaptado a otro modelo sin modificar la arquitectura.
- Todos los componentes están desacoplados y automatizados mediante CI/CD y GitOps.

---

## Autor
Cristian Javier Diaz Alvarez - Pontificia Universidad Javeriana

Fecha: Mayo 2025
