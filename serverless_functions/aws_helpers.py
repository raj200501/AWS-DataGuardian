import boto3
import logging

dynamodb = boto3.resource('dynamodb')

def save_audit_result(table_name, url, audit_result):
    table = dynamodb.Table(table_name)
    response = table.put_item(
        Item={
            "url": url,
            "trackers": audit_result["trackers"],
            "cookies": audit_result["cookies"]
        }
    )
    logging.info(f"Stored audit result for {url}: {response}")
