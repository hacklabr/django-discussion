import django.forms as forms
from .models import Forum

attrs = {'attrs': {'class': 'form-control'}}

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['category', 'title', 'text', 'forum_type', 'is_public', 'groups']
        widgets = {
            'category': forms.Select(**attrs),
            'title': forms.TextInput(**attrs),
            'textarea': forms.Textarea(**attrs),
            'forum_type': forms.Select(**attrs),
            'groups': forms.SelectMultiple(**attrs)
        }
