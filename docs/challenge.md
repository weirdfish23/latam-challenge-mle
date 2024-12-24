# PART I

- Model selection
    - The model selected is `Logistic Regression with Feature Importante and with Balance` because it requires less computational cost to operate in prodcution and provides better interpretability and scalability.
    
# PART II

- FastAPI application 
    - Load model at start up time
    - Schema definition for input body with `pydantic` (`DelayPredictionInputBody` and `Flight` classes)
    - Data preprocessing and missing values filling per request

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
