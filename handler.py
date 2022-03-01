import json
import logging
import os

import boto3


def key(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.getenv('bucketName'))
    objects = bucket.objects.all()
    keys = [obj.key for obj in objects]

    body = {
        "input": event,
        "bucketName": os.getenv("bucketName"),
        "keys": keys
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def file(event, context):
    try:
        name = event['queryStringParameters']['name']

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(os.getenv('bucketName'))
        s3file = bucket.Object(name)
        s3file_content = s3file.get()['Body'].read()

        body = {
            "input": event,
            "bucketName": os.getenv("bucketName"),
            "file": s3file.get(),
            "content": s3file_content
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body, default=str)
        }

    except Exception as e:
        logging.error(e)
        response = {
            "statusCode": 400,
            "message": 'Parameter is invalid : name.' if type(e).__name__ == 'KeyError' else str(e)
        }

    return response
