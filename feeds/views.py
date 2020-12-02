from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from lxml import etree
from .models import Feed, Source

class FeedTodayView(TemplateView):
    template_name='feeds/articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get 'today' feed of current user
        # today feed always exist for user
        today_feed = Feed.objects.get(user=self.request.user, name='today') 
        # get all sources in this feed
        articles = []
        for source in today_feed.sources.all():
            # get rss data by source's link
            rss_text = requests.get(source.url).text
            rss_data = rss_text.encode('utf-8')
            f = open('rss_data_techcrunch.xml', 'w')
            f.write(rss_text)
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            root = etree.fromstring(rss_data, parser=parser)
            titles = root.findall('.//item/title')
            articles += [{'source': source.name, 'title': title.text} for title in titles]
        context['articles'] = articles
        return context
