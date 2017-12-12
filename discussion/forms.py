from django.forms import ModelForm
from .models import Forum

class ForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = ['category', 'title', 'text', 'forum_type', 'is_public', 'groups']
