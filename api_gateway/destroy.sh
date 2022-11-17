gcloud beta api-gateway api-configs delete backend-config --api=backend-api --project=sleep-tracker &&

gcloud beta api-gateway apis delete backend-api --project=sleep-tracker &&

gcloud beta api-gateway gateways delete backend-gateway \
  --location=us-central1 --project=sleep-tracker

