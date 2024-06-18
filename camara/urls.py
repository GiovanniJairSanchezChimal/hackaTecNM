from django.urls import path
from . import views
from .views import index, video, video_stream

urlpatterns = [
    path('', index, name ='index'),
    path('video/', views.video, name='video'),
    path('stream/', views.video_stream, name='video_stream'),
    path('registration/register', views.register, name = 'register')
]