"""
mms_pair URL Configuration
"""

from django.urls import path
from . import views
from .api import viewsets

app_name = 'mms_pair'
urlpatterns = [
    # Index page
    path('', views.index, name='index'),
    # API
    path('api/v1/mms', viewsets.CoinListView.as_view())
]
