#!/bin/bash

docker build -t gcr.io/sleep-tracker/token-cloudrun . &&
docker push gcr.io/sleep-tracker/token-cloudrun &&

gcloud run deploy token-cloudrun \
  --image gcr.io/sleep-tracker/token-cloudrun \
  --region us-central1