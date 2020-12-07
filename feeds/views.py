from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin
import requests
from lxml import etree
import os, json
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile

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
        self.save_articles_data(articles)
        return articles

    def save_articles_data(self, articles_data):
        user_id = self.request.user.id 
        if not os.path.exists(f'{settings.MEDIA_ROOT}/{user_id}'):
            os.mkdir(f'{settings.MEDIA_ROOT}/{user_id}')
        with open(f'{settings.MEDIA_ROOT}/{user_id}/today_feed.json', 'w') as f:
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
        with open(f'{settings.MEDIA_ROOT}/{user_id}/today_feed.json', 'r') as f:
            articles_dict = json.load(f)
            return articles_dict[str(article_id)] 


class SourceListView(ListView):
    model = Source
    template_name = 'feeds/manage_sources.html'
    context_object_name = 'sources_list'

    # return sources for current user from 'today' feed
    def get_queryset(self):
        qs = super().get_queryset()
        today_feed = Feed.objects.get(user=self.request.user, name='today') 
        return today_feed.sources.all()

    def get(self, request, *args, **kwargs):
        print('get request')
        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        source_url = self.request.POST['source_url']

        # get source name and icon url from rss data
        rss_data = requests.get(source_url).text.encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(rss_data, parser=parser)
        
        source_name = root.find('.//channel/title').text
        icon_url = root.find('.//channel/image/url').text
        icon_title = root.find('.//channel/image/title').text

        # save new source in 'today' feed
        new_source = Source(name=source_name, url=source_url)
        new_source.save()
        self.download_source_icon(icon_url, icon_title, new_source)
        today_feed = Feed.objects.get(user=self.request.user, name='today') 
        today_feed.sources.add(new_source)

        return HttpResponseRedirect('')

    def download_source_icon(self, icon_url, icon_title, source):
        icon_response = requests.get(icon_url)
        icon_extension = os.path.splitext(icon_url)[-1]
        icon_filename = f'{icon_title}.{icon_extension}'
        source.icon.save(icon_filename, ContentFile(icon_response.content), save=True)
        #with open(f'{settings.MEDIA_ROOT}/sources_icons/{icon_file}', 'wb') as f:
        #    f.write(icon_page.content)

