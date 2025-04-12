#!/bin/bash

echo ""
echo "🔍 Iniciando verificación del entorno de despliegue..."

# Verificar que gcloud esté instalado
if ! command -v gcloud &> /dev/null; then
  echo "❌ ERROR: 'gcloud' no está instalado. Instalalo desde https://cloud.google.com/sdk"
  exit 1
fi

# Verificar que docker esté instalado
if ! command -v docker &> /dev/null; then
  echo "❌ ERROR: 'docker' no está instalado. Instalalo desde https://docs.docker.com/get-docker/"
  exit 1
fi

# Verificar autenticación en gcloud
AUTH_USER=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
if [[ -z "$AUTH_USER" ]]; then
  echo "❌ ERROR: No estás autenticado en Google Cloud."
  echo "➡️ Ejecutá: gcloud auth login"
  exit 1
else
  echo "✅ Usuario autenticado en gcloud: $AUTH_USER"
fi

# Verificar proyecto seleccionado
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [[ -z "$PROJECT_ID" || "$PROJECT_ID" == "(unset)" ]]; then
  echo "❌ ERROR: No hay un proyecto seleccionado en gcloud."
  echo "➡️ Ejecutá: gcloud config set project TU_PROJECT_ID"
  exit 1
else
  echo "✅ Proyecto activo: $PROJECT_ID"
fi

# Verificar que exista el archivo .env
if [ ! -f .env ]; then
  echo "❌ ERROR: No se encontró el archivo '.env'."
  echo "➡️ Copiá el ejemplo: cp .env.example .env y completalo."
  exit 1
fi

# Cargar variables del archivo .env
export $(cat .env | xargs)

# Validar variables necesarias
MISSING=false
for var in DATASET_ID TABLE_ID REGION; do
  if [[ -z "${!var}" ]]; then
    echo "❌ ERROR: Falta definir $var en el archivo .env"
    MISSING=true
  fi
done

if [ "$MISSING" = true ]; then
  echo "🛑 Por favor completá todas las variables requeridas en .env"
  exit 1
fi

# Mostrar resumen
echo ""
echo "📋 Resumen de configuración:"
echo "   Proyecto GCP:         $PROJECT_ID"
echo "   Dataset de BigQuery: $DATASET_ID"
echo "   Tabla de BigQuery:   $TABLE_ID"
echo "   Región de despliegue: $REGION"
echo "   Service Account:     $SERVICE_ACCOUNT_EMAIL"
echo ""

echo "✅ Entorno validado correctamente."


