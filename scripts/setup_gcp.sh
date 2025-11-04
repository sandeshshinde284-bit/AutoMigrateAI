#!/bin/bash
set -e

echo "?? Setting up Google Cloud..."

# Load variables
source ../.env

# Set project
gcloud config set project $GCP_PROJECT_ID

echo "? GCP setup complete!"
echo "Project: $GCP_PROJECT_ID"
echo "Region: $GCP_REGION"
