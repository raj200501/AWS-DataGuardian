#!/bin/bash
set -euo pipefail

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r dependencies.txt

# Package the Lambda function and shared modules
zip -r lambda.zip main.py audit_privacy.py aws_helpers.py logger.py ../dataguardian venv/
