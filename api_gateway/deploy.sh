gcloud services enable apigateway.googleapis.com &&
gcloud services enable servicemanagement.googleapis.com &&
gcloud services enable servicecontrol.googleapis.com &&

gcloud beta api-gateway apis create backend-api --project=sleep-tracker &&

gcloud beta api-gateway api-configs create backend-config \
  --api=backend-api --openapi-spec=openapi2.yaml \
  --project=sleep-tracker --backend-auth-service-account=burhan@usleep-tracker.iam.gserviceaccount.com &&

gcloud beta api-gateway apis describe backend-api --project=sleep-tracker
