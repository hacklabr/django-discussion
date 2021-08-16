from modeltranslation.translator import register, TranslationOptions
from .models import Forum, Category


@register(Forum)
class ForumTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name','description',)
