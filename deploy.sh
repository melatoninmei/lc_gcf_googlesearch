#!/bin/bash

# Check if the environment variable is set
if [ -z "$REGION" ]; then
  # If not set, use the default value
  REGION="australia-southeast1"
fi

source env.sh

gcloud functions deploy python-http-function \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=hello_http \
    --trigger-http \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CSE_ID=${GOOGLE_CSE_ID},GOOGLE_API_KEY=${GOOGLE_API_KEY},OPENAI_API_KEY=${OPENAI_API_KEY}