import boto3


def send_sms(message, number='+5511945354762'):
    sns = boto3.client("sns")
    return sns.publish(PhoneNumber=number, Message=message)

