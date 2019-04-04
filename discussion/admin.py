from django.contrib import admin
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification


class TopicAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']


admin.site.register(Category)
admin.site.register(Forum)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(TopicNotification)
