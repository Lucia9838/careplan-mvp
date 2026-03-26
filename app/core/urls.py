from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/generate-careplan/', views.generate_careplan, name='generate_careplan'),
]
