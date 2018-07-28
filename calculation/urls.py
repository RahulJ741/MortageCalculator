from django.urls import path, include,re_path
from calculation import views

urlpatterns = [
    path('', views.calculate, name="calculate"),
    re_path('^ajax_request_data', views.ajax_request_data, name='ajax_request_data'),
]
