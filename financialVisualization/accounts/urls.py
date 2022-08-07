from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Login, name='Login'),
    path('register', views.register, name='Register'),
    path('password/<str:token>', views.set_password, name='SetPassword')
]
