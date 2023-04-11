# Third-party Libraries
import boto3
from django.conf import settings

ses_client = boto3.client(
    "ses",
    region_name="us-east-1",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)


def send_email(subject: str, body: str, recipient: str) -> dict:
    """
    Sends an email using Amazon SES (Simple Email Service).

    :param subject: A string representing the subject of the email.
    :param body: A string representing the body of the email.
    :param recipient: A string representing the email address of the recipient.
    :return: A dictionary containing the response from Amazon SES.
    """
    return ses_client.send_email(
        Destination={
            "ToAddresses": [
                recipient,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": "UTF-8",
                    "Data": body,
                },
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": subject,
            },
        },
        Source="sender@example.com",
    )
