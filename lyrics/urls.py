from django.urls import path
from .views import AddSongAPIView

urlpatterns = [
    path('add/', AddSongAPIView.as_view(), name='add_song'),
]