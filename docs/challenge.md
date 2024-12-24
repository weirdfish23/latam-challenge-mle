# PART I

- Model selection
    - The model selected is `Logistic Regression with Feature Importante and with Balance` because it requires less computational cost to operate in prodcution and provides better interpretability and scalability.
    
# PART II

- FastAPI application 
    - Load model at start up time
    - Schema definition for input body with `pydantic` (`DelayPredictionInputBody` and `Flight` classes)
        - It validates:
            - Operator (present in training data)
            - Month (Between 1 and 12)
            - Tipo Vuelo (`N` or `I`)

    - Data preprocessing and fill missing values per request

# PART III - Deploy API

- Create Docker Image repository in Artifact Registry (GCP)
```
gcloud artifacts repositories create demo-fastapi --repository-format docker --project latam-challenge-mle-445621 --location us-central1
```
- Push Docker image
```
gcloud builds submit --config cloudbuild.yaml --project latam-challenge-mle-445621
```
- Run Application in GCRun
```
gcloud run services replace service.yaml --region us-east1
```
- Update policy to make it publicly available
```
gcloud run services set-iam-policy demo-fastapi-service gcr-service-policy.yaml --region us-east1
```

# PART IV - CI/CD

- Continuous deployment (runs on push or pull request to MAIN branch)
    - Build and push docker image to GC Artifact Registry 
    - Deploy latest docker image to GC Run
- Continuous integration (runs on push or pull request to any branch)
    - Test model (`make model-test`)
    - Test api (`make api-test`)
    
Add permissions to service account `latam-challenge` for CD:
```.sh
gcloud projects add-iam-policy-binding latam-challenge-mle-445621 \
    --member="serviceAccount:latam-challenge@latam-challenge-mle-445621.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding latam-challenge-mle-445621 \
  --member="serviceAccount:latam-challenge@latam-challenge-mle-445621.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding latam-challenge-mle-445621 \
  --member="serviceAccount:latam-challenge@latam-challenge-mle-445621.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
  ```

Author: Joel Jossue Cabrera Rios