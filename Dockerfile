FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# File: terraform/main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_codepipeline" "ci_cd_pipeline" {
  name = "api-ci-cd-pipeline"

  # Define pipeline stages here (Source, Build, Deploy)
  # Include S3 bucket, Lambda/EC2 details as required
}
