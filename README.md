# Plataforma ESG 2.0 (Open Source)

Plataforma auditable para la medición de impacto Ambiental, Social y de Gobernanza (ESG) en PYMEs, alineada con los ODS y la directiva CSRD.

## Estructura del Repositorio
- `backend/`: API en FastAPI (`main.py`), modelos SQLAlchemy (`models.py`) y dependencias (`requirements.txt`).
- `frontend/`: Interfaz interactiva (`index.html`).
- `Dockerfile` y `docker-compose.yml`: Contenedores listos para desarrollo local y Google Cloud Run.
- `.github/workflows/deploy-cloudrun.yml`: Pipeline CI/CD para despliegue automático en Google Cloud.
