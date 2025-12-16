import json
import boto3
import urllib3

http = urllib3.PoolManager()
secrets = boto3.client("secretsmanager")

def lambda_handler(event, context):
    secret = secrets.get_secret_value(
        SecretId="sujal/webhook-url"
    )
    secret_dict = json.loads(secret["SecretString"])
    webhook_url = secret_dict["slack-webhook-url"]

    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Where will you work today?*"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "🏢 Working from Office"},
                        "style": "primary",
                        "value": "WFO",
                        "action_id": "wfo"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "🏠 Working Remotely"},
                        "style": "danger",
                        "value": "WFH",
                        "action_id": "wfh"
                    }
                ]
            }
        ]
    }

    http.request(
        "POST",
        webhook_url,
        body=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )

    return {"statusCode": 200}
