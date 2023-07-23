from django.contrib import admin
from BlogApp.models import User, Post, Bookmark, Comment

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Bookmark)
admin.site.register(Comment)
