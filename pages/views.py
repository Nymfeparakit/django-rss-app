from django.shortcuts import render
from django.views.generic import TemplateView
import requests

class IndexView(TemplateView):
    template_name='pages/index.html'

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    f = open("../books_api_key", "r")
    #    api_key = f.read()
    #    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key={api_key}') 
    #    print(response.json())


class AboutView(TemplateView):
    template_name='pages/about.html'
