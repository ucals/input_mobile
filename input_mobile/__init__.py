import os
import boto3
from dotenv import load_dotenv

load_dotenv()


def send_sms(message, number=os.environ["SMS_PHONE"]):
    sns = boto3.client("sns")
    return sns.publish(PhoneNumber=number, Message=message)
