# views.py

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import VideoUploadForm
from .models import Video
import os
from .tasks import process_video,upload_to_s3
import boto3


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']
            video_name = video_file.name
            local_file_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name)
            video_title = request.POST.get('title', '')
            
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            
            with open(local_file_path, 'wb+') as local_file:
                for chunk in video_file.chunks():
                    local_file.write(chunk)

            print(f"Saved video locally at: {local_file_path}")


            # upload_to_s3.delay(video_name,video_title,local_file_path)
            
            s3 = boto3.client('s3',
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_S3_REGION_NAME)
            s3_file_key = f'videos/{video_file.name}'
            with open(local_file_path, 'rb') as file:
                s3.upload_fileobj(file, 'ecowiserproject', s3_file_key)

            print(f"Uploaded video to S3 at: {s3_file_key}")

            
            video = Video.objects.create(
                title=request.POST.get('title', ''),
                video_file=s3_file_key,  
                local_path=local_file_path  
            )

            print(f"Created video instance with local path: {local_file_path}")

            
            process_video.delay(video.id)
            
            return redirect('search')
    else:
        form = VideoUploadForm()
    
    return render(request, 'videos/upload.html', {'form': form})


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/list.html', {'videos': videos})


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        try:
            dynamodb_client = boto3.client(
                'dynamodb',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            table_name = 'SubtitleData'

            response = dynamodb_client.scan(
                TableName=table_name,
                FilterExpression="contains(#txt, :query)",
                ExpressionAttributeNames={
                    '#txt': 'text'
                },
                ExpressionAttributeValues={
                    ':query': {'S': query}
                }
            )

            for item in response.get('Items', []):
                subtitle_id = item.get('subtitle_id', {}).get('S')
                video_id = item.get('video_id', {}).get('S')
                start_time = float(item.get('startTime', {}).get('N'))
                end_time = float(item.get('endTime', {}).get('N'))
                text = item.get('text', {}).get('S')

                video2 = Video.objects.get(id=video_id)
                print(video2)

                # Optionally, retrieve related Video object if needed
                # video = Video.objects.get(id=video_id)

                # Create a dictionary representation of the result
                result_dict = {
                    'video_title': f'{video2.title}',  # Adjust as per your Video model
                    'text': text,
                    'start_time': start_time,
                    'end_time': end_time,
                }
                results.append(result_dict)
                print(results)

        except boto3.exceptions.Boto3Error as e:
            print(f"Error querying DynamoDB table {table_name}: {str(e)}")

    return render(request, 'videos/search.html', {'results': results, 'query': query})
































    # srt_files = glob.glob(os.path.join(video_dir, f'{file_name_without_extension}*.srt'))

    # def parse_time(time_str):
    #     h, m, s = time_str.replace(',', '.').split(':')
    #     return float(h) * 3600 + float(m) * 60 + float(s)

    # for srt_file in srt_files:
    #     if os.path.getsize(srt_file) > 0:
    #         with open(srt_file, 'r', encoding='utf-8') as f:
    #             lines = f.readlines()
    #             for i in range(0, len(lines)):
    #                 line = lines[i].strip()
    #                 if '-->' in line:
    #                     try:
    #                         start_time, end_time = line.split(' --> ')
    #                         text = lines[i + 1].strip()
    #                         subtitle = Subtitle(
    #                             video=video,
    #                             text=text,
    #                             start_time=parse_time(start_time),
    #                             end_time=parse_time(end_time)
    #                         )
    #                         subtitle.save()
    #                     except ValueError:
    #                         continue  
    #                     except IndexError:
    #                         continue 
    #     else:
    #         # Remove empty subtitle file
    #         os.remove(srt_file)