from django.contrib import admin

from .models import Author, Comment, News
# from .. import simpleapp

admin.site.register(News)
admin.site.register(Author)
admin.site.register(Comment)
