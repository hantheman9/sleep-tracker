gcloud services enable backend-api-21s9fc0577yxd.apigateway.sleep-tracker.cloud.goog &&

gcloud beta api-gateway gateways create backend-gateway \
  --api=backend-api --api-config=backend-config \
  --location=us-central1 --project=sleep-tracker &&

gcloud beta api-gateway gateways describe backend-gateway \
  --location=us-central1 --project=sleep-tracker

