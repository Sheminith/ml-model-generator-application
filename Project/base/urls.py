from django.urls import path
from base import views

urlpatterns = [
    path('', views.upload_dataset, name='upload_dataset'),
    path('train/<str:pk>/', views.train_model, name='train_model'),
]