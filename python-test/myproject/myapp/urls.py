from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transcribe/', views.transcribe, name='transcribe'),  # Assurez-vous que cette ligne est correcte
]
