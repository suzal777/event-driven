import json
import os
import boto3
import urllib.parse
import base64
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
ses = boto3.client("ses", region_name="us-east-1")

table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    # ADD THIS FIRST (CRITICAL)
    print("RAW EVENT:", json.dumps(event))

    # ---- safe body handling ----
    body = event.get("body", "")
    if not body:
        return {"statusCode": 400, "body": "Missing body"}

    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")

    parsed_body = urllib.parse.parse_qs(body)

    if "payload" not in parsed_body:
        print("PARSED BODY:", parsed_body)
        return {
            "statusCode": 200,
            "body": json.dumps({"text": "⚠️ Unsupported Slack request"})
        }

    payload = json.loads(parsed_body["payload"][0])

    # ---- existing logic continues ----
    user = payload["user"]["username"]
    slack_user_id = payload["user"]["id"]
    mode = payload["actions"][0]["value"]

    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")

    table.put_item(
        Item={
            "date": date,
            "username": user,
            "mode": mode,
            "timestamp": now.isoformat(),
            "slackUserId": slack_user_id,
            "ttl": int(now.timestamp()) + 86400 * 30
        }
    )

    subject = "Office Attendance Confirmation" if mode == "WFO" else "Remote Work Confirmation"
    body_text = (
        "Thanks for confirming your office presence today."
        if mode == "WFO"
        else "Your remote work status has been recorded."
    )

    ses.send_email(
        Source=os.environ["EMAIL_SENDER"],
        Destination={"ToAddresses": [os.environ["EMAIL_DOMAIN"]]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body_text}}
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": f"✅ Thanks {user}, your response ({mode}) is recorded."
        })
    }
