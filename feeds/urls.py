from django.urls import path 

from . import views

urlpatterns = [
    path('today/', views.FeedTodayView.as_view(), name='today'),
    #path('article/<article_title>', views.ArticleDetailView.as_view(), name='article'),
    path('article/<int:article_id>', views.ArticleDetailView.as_view(), name='article'),
]