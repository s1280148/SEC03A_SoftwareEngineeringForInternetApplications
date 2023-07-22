from django.contrib import admin
from BlogApp.models import User, Post, Bookmark

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Bookmark)
