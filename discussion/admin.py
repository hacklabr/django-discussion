from django.contrib import admin
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification

admin.site.register(Category)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(TopicNotification)
