"""
mms_pair URL Configuration
"""

from django.urls import path
from . import views

app_name = 'mms_pair'
urlpatterns = [
    path('', views.index, name='index'),
]
