#!/bin/bash

docker build -t gcr.io/sleep-tracker/etl-cloudrun . &&
docker push gcr.io/sleep-tracker/etl-cloudrun &&

gcloud run deploy etl-cloudrun --no-allow-unauthenticated \
  --image gcr.io/sleep-tracker/etl-cloudrun \
  --region us-central1 --platform managed