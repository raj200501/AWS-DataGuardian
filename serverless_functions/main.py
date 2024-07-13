import json
import logging
from audit_privacy import perform_privacy_audit
from aws_helpers import save_audit_result

def lambda_handler(event, context):
    body = json.loads(event["body"])
    url = body["url"]
    logging.info(f"Received URL: {url}")

    # Perform privacy audit
    audit_result = perform_privacy_audit(url)

    # Store result in DynamoDB
    save_audit_result("PrivacyAuditTable", url, audit_result)

    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Audit completed", "result": audit_result})
    }
    return response
