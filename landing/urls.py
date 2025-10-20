from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('media/videos/<str:filename>', views.stream_video, name='stream_video'),
]
