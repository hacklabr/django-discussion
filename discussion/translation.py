from modeltranslation.translator import register, TranslationOptions
from .models import Topic, Forum


@register(Forum)
class ForumTranslationOptions(TranslationOptions):
    fields = ('title',)
