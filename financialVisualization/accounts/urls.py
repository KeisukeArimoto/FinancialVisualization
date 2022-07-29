from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Login, name='Login'),
    path('logout', views.Logout, name='Logout'),
    path('register', views.register, name='Register'),
    path('password', views.set_password, name='SetPassword')
]
