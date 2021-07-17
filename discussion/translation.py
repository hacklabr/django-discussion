from modeltranslation.translator import register, TranslationOptions
from .models import Topic, Forum


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'slug',)

@register(Forum)
class ForumTranslationOptions(TranslationOptions):
    fields = ('title', 'text', 'slug',)
