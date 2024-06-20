
from django.urls import path
from . import  views
urlpatterns = [
    path('', views.upload_video, name='upload_video'),
    path('list/', views.video_list, name='video_list'),
    path('search/', views.search, name='search'),
]