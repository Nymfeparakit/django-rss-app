from django.shortcuts import render
from django.views.generic import TemplateView

class FeedTodayView(TemplateView):
    template_name='feeds/articles.html'
