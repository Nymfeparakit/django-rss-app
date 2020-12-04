from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from lxml import etree
import os, json
from django.conf import settings

from .models import Feed, Source

class FeedTodayView(TemplateView):
    template_name='feeds/articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get 'today' feed of current user
        # today feed always exist for user
        today_feed = Feed.objects.get(user=self.request.user, name='today') 
        # get all sources in this feed
        context['articles_dict'] = self.parse_feed_articles(today_feed)
        return context

    def parse_feed_articles(self, feed):
        # dict will have structure like this
        # { id: { 'title': '...', 'desc': '...' } }
        articles = {}
        for source in feed.sources.all():
            # get rss data by source's link
            rss_data = requests.get(source.url).text.encode('utf-8')
            if source.name == 'habr':
                rss_text = requests.get(source.url).text
                with open('habr_feed.xml', 'w') as f:
                    f.write(rss_text)
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            root = etree.fromstring(rss_data, parser=parser)
            titles = root.findall('.//item/title')
            descriptions = root.findall('.//item/description')
            for title, desc in zip(titles, descriptions):
                articles[abs(hash(title.text))] = {
                    'title': title.text,
                    'description': desc.text,
                    'source': source.name
                }
            # articles += [
            # {'title': title.text, 
            # 'id': abs(hash(title.text)), # TODO изменить id статьи?
            # 'description': desc.text,
            # 'source': source.name} 
            # for title, desc in zip(titles, descriptions) ]
        self.save_articles_data(articles)
        return articles

    def save_articles_data(self, articles_data):
        user_id = self.request.user.id 
        if not os.path.exists(f'{settings.MEDIA_ROOT}/{user_id}'):
            os.mkdir(f'{settings.MEDIA_ROOT}/{user_id}')
        with open(f'{settings.MEDIA_ROOT}/{user_id}/today_feed.json', 'w') as f:
            print("saving articles data")
            json.dump(articles_data, f, ensure_ascii=False)


class ArticleDetailView(TemplateView):
    template_name='feeds/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_id = kwargs['article_id']
        context['article'] = self.read_article_data(article_id)
        return context

    def read_article_data(self, article_id):
        user_id = self.request.user.id
        with open(f'{user_id}/today_feed.json', 'r') as f:
            articles_dict = json.load(f)
            return articles_dict[str(article_id)] 


