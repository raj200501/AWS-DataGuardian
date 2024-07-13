#!/bin/bash

# Validate the SAM template
sam validate --template-file sam_template.yaml

# Package the SAM template
sam package --template-file sam_template.yaml --output-template-file packaged.yaml --s3-bucket YOUR_S3_BUCKET_NAME

# Deploy the SAM template
sam deploy --template-file packaged.yaml --stack-name DataGuardian --capabilities CAPABILITY_IAM
