#!/bin/bash

# Validación del entorno (setup.sh)
./setup.sh
if [ $? -ne 0 ]; then
  echo "❌ Error: Validación fallida."
  exit 1
fi

echo "✅ Validación superada. Continuando con build y deploy..."

set -a
source .env
set +a
echo "🔍 Variables cargadas:"
echo "PROJECT_ID: $PROJECT_ID"
echo "DATASET_ID: $DATASET_ID"
echo "TABLE_ID: $TABLE_ID"
echo "REGION: $REGION"


PROJECT_ID=$(gcloud config get-value project)
REPO_NAME="yogonet-repo"
SERVICE_NAME="yogonet-scraper"
REGION=${REGION:-us-central1}
IMAGE_NAME="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME"

# Build Docker image
echo "🔧 Construyendo imagen Docker..."
docker build -t $IMAGE_NAME .

# Configurar autenticación de Docker
echo "🔐 Configurando autenticación Docker..."
gcloud auth configure-docker $REGION-docker.pkg.dev

# Push a Artifact Registry
echo "📦 Subiendo imagen a Artifact Registry..."
docker push $IMAGE_NAME

# Crear Cloud Run Job (si no existe)
echo "🛠️ Creando Cloud Run Job (si no existe)..."
gcloud beta run jobs describe $SERVICE_NAME --region=$REGION &> /dev/null

if [ $? -ne 0 ]; then
  gcloud beta run jobs create $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --memory 512Mi \
    --set-env-vars PROJECT_ID=$PROJECT_ID,DATASET_ID=$DATASET_ID,TABLE_ID=$TABLE_ID
else
  echo "🔄 Actualizando imagen del Job..."
gcloud beta run jobs update $SERVICE_NAME \
  --image $IMAGE_NAME \
  --region $REGION \
  --memory 1024Mi \
  --set-env-vars PROJECT_ID=$PROJECT_ID,DATASET_ID=$DATASET_ID,TABLE_ID=$TABLE_ID
fi

# Ejecutar el job
echo "🚀 Ejecutando Job en Cloud Run..."
gcloud beta run jobs execute $SERVICE_NAME --region $REGION

echo "✅ Job ejecutado correctamente."
