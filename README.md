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
│   │   └── train_model.py              # Script para entrenar y guardar el modelo
│   ├── Dockerfile
│   └── requirements.txt
├── loadtester/
│   ├── main.py                         # Script que genera peticiones aleatorias a /predict
│   ├── Dockerfile
│   └── requirements.txt
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
├── argocd-install.yaml                 # Archivo de instalación de Argo CD
└── train_model.py                      # Script principal para entrenar el modelo
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

## Requisitos Previos

- Kubernetes cluster configurado y funcionando
- Docker instalado y configurado
- Argo CD instalado (se puede instalar usando el archivo `argocd-install.yaml`)
- Acceso a GitHub Container Registry (GHCR)
- Python 3.x
- kubectl configurado con acceso al cluster

---

## Instrucciones de Instalación

1. **Instalar Argo CD**:
   ```bash
   kubectl apply -f argocd-install.yaml
   ```

2. **Configurar GitHub Container Registry**:
   - Crear un token de acceso personal en GitHub con permisos para el registro
   - Crear un secreto en Kubernetes:
     ```bash
     kubectl create secret docker-registry ghcr-secret \
       --docker-server=ghcr.io \
       --docker-username=<tu-usuario> \
       --docker-password=<tu-token> \
       --docker-email=<tu-email>
     ```

3. **Desplegar la Aplicación**:
   ```bash
   kubectl apply -f argo-cd/app.yaml
   ```

---

## Guía de Uso

### Acceso a la API
La API está expuesta a través de un servicio Kubernetes. Para acceder localmente:
```bash
kubectl port-forward svc/api 8081:80
```
La API estará disponible en `http://localhost:8081` con los siguientes endpoints:
- `/predict`: Para realizar predicciones
- `/metrics`: Para ver las métricas de Prometheus

### Acceso a Grafana
```bash
kubectl port-forward svc/grafana 3000:3000
```
Acceder a `http://localhost:3000` (credenciales por defecto: admin/admin)

### Acceso a Prometheus
```bash
kubectl port-forward svc/prometheus 9090:9090
```
Acceder a `http://localhost:9090`

---

## Solución de Problemas

### Problemas de Conexión con la API
Si el port-forwarding falla con el error "Connection refused":
1. Verificar que el pod de la API está corriendo:
   ```bash
   kubectl get pods -l app=api
   ```
2. Verificar los logs del pod:
   ```bash
   kubectl logs -l app=api
   ```
3. Asegurarse que el servicio está correctamente configurado:
   ```bash
   kubectl get svc api
   ```

### Problemas con Métricas
Si las métricas no aparecen en Grafana:
1. Verificar que Prometheus está scrapeando correctamente:
   ```bash
   kubectl get pods -l app=prometheus
   kubectl logs -l app=prometheus
   ```
2. Verificar la configuración de Prometheus:
   ```bash
   kubectl get configmap prometheus-config -o yaml
   ```

### Problemas con Argo CD
Si la sincronización no funciona:
1. Verificar el estado de la aplicación en Argo CD:
   ```bash
   kubectl get applications -n argocd
   ```
2. Revisar los logs de Argo CD:
   ```bash
   kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller
   ```

---

## Autor
Cristian Javier Diaz Alvarez - Pontificia Universidad Javeriana

Fecha: Mayo 2025
