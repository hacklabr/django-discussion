import django.forms as forms
from .models import Forum

attrs = {'attrs': {'class': 'form-control'}}

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['category', 'title', 'text', 'is_public', 'groups']
        widgets = {
            'category': forms.SelectMultiple(**attrs),
            'title': forms.TextInput(**attrs),
            'textarea': forms.Textarea(**attrs),
            'groups': forms.SelectMultiple(**attrs)
        }
