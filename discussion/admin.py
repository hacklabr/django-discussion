from django.contrib import admin
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification


class ForumAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'groups',
        'category',
    ]
    search_fields = [
        'title',
        'text',
    ]

class TopicAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']


admin.site.register(Category)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(TopicNotification)
