# urls.py

from django.urls import path
from .views import mec_reward

urlpatterns = [
    path('<int:pk>/', mec_reward, name='mec'),
]
