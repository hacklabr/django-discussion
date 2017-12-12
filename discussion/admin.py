from django.contrib import admin
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification


class TopicAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']


class ForumAdmin(admin.ModelAdmin):
    list_filter = ['groups__contracts']

admin.site.register(Category)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(TopicNotification)
