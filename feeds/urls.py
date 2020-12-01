from django.urls import path 

from . import views

urlpatterns = [
    path('today/', views.FeedTodayView.as_view(), name='today'),
]