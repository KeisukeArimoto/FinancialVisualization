from django.urls import path
from .views import views

urlpatterns = [
    path('admin', views.show_management_view, name='show_management_view'),
    path('saveSpecifiedDate', views.save_specified_date, name='save_specified_date')
]