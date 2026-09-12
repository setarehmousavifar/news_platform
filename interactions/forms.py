from django import forms
from django.core.exceptions import ValidationError

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        labels = {'content': 'Comment Text'}
        widgets = {
            'parent': forms.HiddenInput(),
        }

    def clean_content(self):
        content = (self.cleaned_data.get('content') or '').strip()
        if len(content) < 2:
            raise ValidationError('Comment must be at least 2 characters.')
        if len(content) > 2000:
            raise ValidationError('Comment must be at most 2000 characters.')
        return content

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent and parent.parent_id is not None:
            raise ValidationError('Only one-level replies are allowed.')
        return parent
