from __future__ import print_function

import os
import json
import urllib
import boto3

print('Loading function')

s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    images_bucket = event['Records'][0]['s3']['bucket']['name']
    images_key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        reko_response = rekognition.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': images_bucket,
                    'Name': images_key,
                },
            },
            Attributes=[
                'ALL',
                ]
        )

        label_records = ''
        for label in reko_response['FaceDetails'] :
            label_record = []
            label_record.append(label["Smile"])
            label_record.append(label["Emotions"])
            label_record.append(label["EyesOpen"])
            label_record.append(label["MouthOpen"])

            label_records = label_records + ','.join(map(str, label_record)) + '\n'


        results_bucket = s3.Bucket('mitsu-face-rekognition')
        s3_response = results_bucket.put_object( \
            ACL='private', \
            Body=label_records, \
            Key=images_key + ".csv", \
            ContentType='text/plain' \
        )
        return str(s3_response)
    except Exception as e:
        print(e)
        raise e
