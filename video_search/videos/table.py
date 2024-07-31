import os
import boto3
from django.conf import settings



dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_S3_REGION_NAME,
                                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


table_name = 'SubtitleData'
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'subtitle_id',
            'KeyType': 'HASH'  
        },
        {
            'AttributeName': 'video_id',
            'KeyType': 'RANGE'  
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'subtitle_id',
            'AttributeType': 'S' 
        },
        {
            'AttributeName': 'video_id',
            'AttributeType': 'S'  
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)


table.meta.client.get_waiter('table_exists').wait(TableName=table_name)


print(f"Table {table_name} created successfully!")






