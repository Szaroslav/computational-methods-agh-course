from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init),
    path('create/', views.create_file),
    path('count/', views.count)
]