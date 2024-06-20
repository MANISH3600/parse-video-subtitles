import os
import boto3
from django.conf import settings
# AWS credentials

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_S3_REGION_NAME,
                                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

# Example DynamoDB table definition
table_name = 'SubtitleData'
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'subtitle_id',
            'KeyType': 'HASH'  # Partition key
        },
        {
            'AttributeName': 'video_id',
            'KeyType': 'RANGE'  # Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'subtitle_id',
            'AttributeType': 'S'  # S stands for String
        },
        {
            'AttributeName': 'video_id',
            'AttributeType': 'S'  # S stands for String
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

# Print table details
print(f"Table {table_name} created successfully!")










# AWS credentials


# # Initialize DynamoDB resource
# dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_S3_REGION_NAME,
#                           aws_access_key_id=AWS_ACCESS_KEY_ID,
#                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# # Example DynamoDB table definition
# table_name = 'SubtitleData'
# table = dynamodb.create_table(
#     TableName=table_name,
#     KeySchema=[
#         {
#             'AttributeName': 'subtitle_id',
#             'KeyType': 'HASH'  # Partition key
#         },
#         {
#             'AttributeName': 'video_id',
#             'KeyType': 'RANGE'  # Sort key
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'subtitle_id',
#             'AttributeType': 'S'  # S stands for String
#         },
#         {
#             'AttributeName': 'video_id',
#             'AttributeType': 'S'  # S stands for String
#         },
#         {
#             'AttributeName': 'text',
#             'AttributeType': 'S'  # S stands for String
#         },
#         {
#             'AttributeName': 'start_time',
#             'AttributeType': 'N'  # N stands for Number (Start time in seconds)
#         },
#         {
#             'AttributeName': 'end_time',
#             'AttributeType': 'N'  # N stands for Number (End time in seconds)
#         },
#         {
#             'AttributeName': 'processed_timestamp',
#             'AttributeType': 'N'  # N stands for Number (Processed timestamp)
#         }
#         # Add more attribute definitions as needed
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )

# # Wait until the table exists
# table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

# # Print table details
# print(f"Table {table_name} created successfully!")
