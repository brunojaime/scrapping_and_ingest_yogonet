#!/bin/bash

# Validación del entorno
./setup.sh
if [ $? -ne 0 ]; then
  echo "Error: Validación fallida."
  exit 1
fi

echo "Validación superada. Continuando con build y deploy..."

# Cargar variables desde .env
set -a
source .env
set +a

# Configuración
PROJECT_ID=$(gcloud config get-value project)
REGION=${REGION:-us-central1}
REPO_NAME=${REPO_NAME:-yogonet-repo}
SERVICE_NAME=${SERVICE_NAME:-yogonet-scraper}
IMAGE_NAME="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME"

echo "Variables cargadas:"
echo "PROJECT_ID=$PROJECT_ID"
echo "DATASET_ID=$DATASET_ID"
echo "TABLE_ID=$TABLE_ID"
echo "REGION=$REGION"
echo "REPO_NAME=$REPO_NAME"
echo "SERVICE_NAME=$SERVICE_NAME"

# Verificar que el repositorio de Artifact Registry exista
echo "Verificando repositorio en Artifact Registry..."
if ! gcloud artifacts repositories describe $REPO_NAME --location=$REGION &>/dev/null; then
  echo "Repositorio $REPO_NAME no existe. Creando..."
  gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Repositorio Docker para el proyecto Yogonet"
else
  echo "Repositorio $REPO_NAME ya existe."
fi

# Build Docker image
echo "Construyendo imagen Docker..."
docker build -t $IMAGE_NAME .

# Configurar autenticación Docker
echo "Configurando autenticación Docker..."
gcloud auth configure-docker $REGION-docker.pkg.dev

# Push a Artifact Registry
echo "Subiendo imagen a Artifact Registry..."
docker push $IMAGE_NAME

# Crear o actualizar Cloud Run Job
echo "Verificando Job..."
gcloud beta run jobs describe $SERVICE_NAME --region=$REGION &>/dev/null

if [ $? -ne 0 ]; then
  echo "Creando nuevo Job en Cloud Run..."
  gcloud beta run jobs create $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --memory 1024Mi \
    --set-env-vars PROJECT_ID=$PROJECT_ID,DATASET_ID=$DATASET_ID,TABLE_ID=$TABLE_ID
else
  echo "Actualizando Job existente..."
  gcloud beta run jobs update $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --memory 1024Mi \
    --set-env-vars PROJECT_ID=$PROJECT_ID,DATASET_ID=$DATASET_ID,TABLE_ID=$TABLE_ID
fi

# Ejecutar el Job
echo "Ejecutando Job en Cloud Run..."
gcloud beta run jobs execute $SERVICE_NAME --region=$REGION

echo "Job ejecutado correctamente."
