from django.urls import path

from . import views


app_name = 'visualizeData'

urlpatterns = [
    path('home', views.Home, name='Home'),
]
