import json
import logging

from serverless_functions.audit_privacy import perform_privacy_audit
from serverless_functions.aws_helpers import save_audit_result


def lambda_handler(event, context):
    body = json.loads(event["body"])
    url = body["url"]
    logging.info("Received URL: %s", url)

    audit_result = perform_privacy_audit(url)
    save_audit_result("PrivacyAuditTable", url, audit_result)

    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Audit completed", "result": audit_result}),
    }
    return response
