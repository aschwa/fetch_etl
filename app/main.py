import localstack_client.session as boto3
import json
from datetime import datetime as dt
from models import UserLogin
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from config import settings
from cryptography.fernet import Fernet

from database import write_login

app = FastAPI()


def encrypt_login(message_body):
    """Processes message from SQS, encrypt
    Args:
        message_body (dict): Message body received from SQS

    Returns:
        UserLogin: user login object with masked ip and device id values,
        current app version and today's date
    """
    key = settings.FERNET_KEY
    f = Fernet(key)
    masked_id = f.encrypt(bytes(message_body["ip"], "utf-8"))
    masked_ip = f.encrypt(bytes(message_body["device_id"], "utf-8"))

    message_body["masked_ip"] = masked_ip
    message_body["masked_device_id"] = masked_id
    message_body["create_date"] = dt.today().date()
    message_body["app_version"] = settings.APP_VERSION
    del message_body["ip"]
    del message_body["device_id"]
    return UserLogin(**message_body)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    """Redirect sphinx docs page for development in GUI"""
    return RedirectResponse(url="/docs")


@app.get("/sqs/}")
def read_sqs_write_postgres() -> UserLogin:
    """
    Reads a message from sqs queue, encrypts PII data,
    saves to Postgres database.

    Returns:
        UserLogin: _description_
    """

    # Get message and receipt handle from sqs
    sqs_client = boto3.client("sqs")
    queue_url = settings.SQS_QUEUE
    response = sqs_client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=1
    )
    message = response["Messages"][0]
    message_body = json.loads(message["Body"])
    receipt_handle = message["ReceiptHandle"]

    # Encrypt PII and save login to postgresql
    encrypted_login = encrypt_login(message_body)
    write_login(encrypted_login)

    # Delete message from sqs now that record has been saved
    response = sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle,
    )

    # Return encrypted data to app For development purposes
    return encrypted_login
