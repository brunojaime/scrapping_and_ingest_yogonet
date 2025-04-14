
# Yogonet Web Scraper – Cloud Run Job

Este proyecto ejecuta un proceso automatizado de scraping en el portal [Yogonet](https://www.yogonet.com/international/), procesa los datos y los carga en BigQuery. Está completamente Dockerizado y desplegado como un **Cloud Run Job**.

---

## ¿Qué hace?

1. Usa Selenium para scrapear noticias desde Yogonet.
2. Procesa los datos con Pandas (conteo de palabras, caracteres, etc.).
3. Inserta los resultados en una tabla de BigQuery.
4. Corre como un Job en Cloud Run con una imagen Docker personalizada.

---

## Requisitos previos

- Tener configurado Google Cloud CLI (`gcloud`) y estar autenticado.
- Permisos para:
  - Crear repos en Artifact Registry
  - Usar Cloud Run y BigQuery
- Habilitar las siguientes APIs:

En bash:
gcloud services enable artifactregistry.googleapis.com run.googleapis.com bigquery.googleapis.com

Instalación y configuración
1. Clonar el repositorio
git clone https://github.com/<usuario>/yogonet-scraper.git
cd yogonet-scraper
2. Crear archivo .env
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:
PROJECT_ID=<tu-id-de-proyecto>
DATASET_ID=news_data
TABLE_ID=yogonet_articles
REGION=us-central1
REPO_NAME=yogonet-repo
SERVICE_NAME=yogonet-scraper
Asegurate de que PROJECT_ID coincida con el proyecto activo que devuelve este comando:
gcloud config get-value project
Despliegue
Ejecutá el siguiente script para construir, subir y correr todo automáticamente:
./deploy.sh

Este script:
- Verifica tu entorno (gcloud, docker, variables)
- Construye y sube la imagen Docker
- Crea o actualiza el Cloud Run Job
- Ejecuta el Job con los valores del archivo .env
Ver resultados
Consultar ejecuciones del Job

gcloud beta run jobs executions list --region=us-central1 --job=yogonet-scraper
También podés verlos en la consola web de Google Cloud.

Ver datos en BigQuery
Ingresá al proyecto en BigQuery y consultá el dataset y tabla definidos en tu .env.
