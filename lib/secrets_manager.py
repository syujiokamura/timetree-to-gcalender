import os
import json
from typing import TypedDict
import boto3

secrets = boto3.client(
    service_name='secretsmanager',
    region_name='ap-northeast-1'
)


class SecretsValues(TypedDict):
    TIMETREE_PERSONAL_TOKEN: str
    CALENDER_NAME: str
    GOOGLE_CALENDER_ID: str


def get_gcp_service_role_json() -> dict:
    res = secrets.get_secret_value(
        SecretId=os.environ['GCP_CALENDER_SERVICE_ROLE_SECRETS_ID']
    )['SecretString']
    return json.loads(res)


def get_secrets_values() -> SecretsValues:
    res = secrets.get_secret_value(
        SecretId=os.environ['TIMETREE_SECRETS_ID']
    )['SecretString']
    return json.loads(res)
