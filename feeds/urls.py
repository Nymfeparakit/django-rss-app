from django.urls import path 

from . import views

urlpatterns = [
    path('today/', views.FeedTodayView.as_view(), name='today'),
    path('article/<int:article_id>', views.ArticleDetailView.as_view(), name='article'),
    path('manage-sources/', views.SourceListView.as_view(), name='manage-sources'),
]