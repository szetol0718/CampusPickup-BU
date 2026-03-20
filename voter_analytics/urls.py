# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 3/20/2026
# Description: URL patterns for voter analytics.

from django.urls import path
from .views import VoterListView, VoterDetailView, VoterGraphsView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path('graphs', VoterGraphsView.as_view(), name='graphs'),
]