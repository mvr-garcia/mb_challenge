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
    # API - List all entrys in Database
    path('api/v1/mms', viewsets.CoinListView.as_view()),
    # API - When all parameters are passed
    path(r'api/v1/<str:crypto>/mms/from=<int:past>&to=<int:now>', viewsets.CryptoListView.as_view()),
    # API - When the final timestamps are not passed
    path(r'api/v1/<str:crypto>/mms/from=<int:past>', viewsets.CryptoListView.as_view()),
]
