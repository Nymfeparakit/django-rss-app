from django.db import models
from django.conf import settings

class Feed(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sources = models.ManyToManyField('Source')

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ImageField(upload_to='sources_icons/')
    url = models.URLField()

    def __str__(self):
        return self.name
