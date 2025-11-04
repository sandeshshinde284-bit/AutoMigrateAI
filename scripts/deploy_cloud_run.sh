#!/bin/bash
set -e

echo "?? Deploying to Cloud Run..."

source ../.env

# Build and push image
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/automigrateai-proxy

# Deploy to Cloud Run
gcloud run deploy automigrateai-proxy \
  --image gcr.io/$GCP_PROJECT_ID/automigrateai-proxy \
  --platform managed \
  --region $GCP_REGION \
  --allow-unauthenticated

echo "? Deployment complete!"
