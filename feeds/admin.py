from django.contrib import admin
from .models import Feed, Source

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
