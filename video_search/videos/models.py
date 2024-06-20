from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    local_path = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField()
    start_time = models.FloatField()
    end_time =models.FloatField(null = True)

    def __str__(self):
        return f"{self.video.title} - {self.text[:50]}"
