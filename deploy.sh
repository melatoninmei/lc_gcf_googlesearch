#!/bin/bash
# source env.sh

# # Check if all the the environment variable are set
# if [ -z "$REGION" ] || [ -z "$GOOGLE_CSE_ID" ] || [ -z "$GOOGLE_API_KEY" ] || [ -z "OPENAI_API_KEY" ]; then
#   echo "Please set all the environment variables in env.sh"
#   exit 1
# fi

gcloud functions deploy google-search-ai-http \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=google_search \
    --trigger-http \
    --memory=512MB \
    --allow-unauthenticated \
    --set-secrets "GOOGLE_CSE_ID=GOOGLE_CSE_ID:latest,GOOGLE_API_KEY=GOOGLE_API_KEY:latest,OPENAI_API_KEY=OPENAI_API_KEY:latest"