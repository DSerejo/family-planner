docker build -t gcr.io/serene-smoke-429712-n5/family-planner-api .
docker push gcr.io/serene-smoke-429712-n5/family-planner-api

gcloud run deploy family-planner-api \
  --image gcr.io/serene-smoke-429712-n5/family-planner-api \
  --platform managed \
  --allow-unauthenticated \
  --region=us-west1 \
  --update-env-vars $(grep -v '^#' .env.staging | grep -v '^[[:space:]]*$' | tr '\n' ',' | sed 's/,$//')
