import os
import glob
from celery import shared_task
from .models import Video, Subtitle 
from django.conf import settings
import subprocess
import boto3
from .models import Video

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video_path = video.local_path  

    
    print(f"Video path: {video_path}")

    video_dir = os.path.dirname(video_path)  
    base_name = os.path.basename(video_path)  
    file_name_without_extension = os.path.splitext(base_name)[0]
    extractor_path = 'ccextractor/ccextractorwinfull.exe'


    if not os.path.exists(video_path):
        print(f"Video file does not exist at: {video_path}")
        return
    
    print(f"Running CCExtractor on video: {video_path}")
    

    subprocess.run([extractor_path, video_path])
    
    print(f"Looking for SRT files in: {video_dir}")
  
    srt_files = glob.glob(os.path.join(video_dir, f'{file_name_without_extension}*.srt'))
    

    dynamodb_client = boto3.client(
        'dynamodb',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    table_name = 'SubtitleData'

    def parse_time(time_str):
        h, m, s = time_str.replace(',', '.').split(':')
        return float(h) * 3600 + float(m) * 60 + float(s)

    for srt_file in srt_files:
        if os.path.getsize(srt_file) > 0:
            with open(srt_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i in range(0, len(lines)):
                    line = lines[i].strip()
                    if '-->' in line:
                        try:
                            start_time, end_time = line.split(' --> ')
                            text = lines[i + 1].strip()
                            subtitle = Subtitle(
                                video=video,
                                text=text,
                                start_time=parse_time(start_time),
                                end_time=parse_time(end_time)
                            )
                            subtitle.save()
                            print(f"Saving subtitle to DynamoDB: {text}")
                            dynamodb_client.put_item(
                                TableName=table_name,
                                Item={
                                    'subtitle_id': {'S': str(subtitle.id)},
                                    'video_id': {'S': str(video.id)},
                                    'startTime': {'N': str(parse_time(start_time))},
                                    'endTime': {'N': str(parse_time(end_time))},
                                    'text': {'S': text},
                                }
                            )
                        except (ValueError, IndexError):
                            continue
        else:
            os.remove(srt_file)
            print(f"Removed empty SRT file: {srt_file}")



@shared_task
def upload_to_s3(video_name,video_title,local_file_path):
    

    
    s3 = boto3.client('s3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME)
    s3_file_key = f'videos/{video_name}'
    with open(local_file_path, 'rb') as file:
        s3.upload_fileobj(file, 'ecowiserproject', s3_file_key)

    print(f"Uploaded video to S3 at: {s3_file_key}")

    
    video = Video.objects.create(
        title=video_title,
        video_file=s3_file_key,  
        local_path=local_file_path  
    )
    print(video)

    print(f"Created video instance with local path: {local_file_path}")
    process_video.delay(video.id)
