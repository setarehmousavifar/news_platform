from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']  # Form fields including comment content and parent comment
        labels = {'content': 'Comment Text'}  # Label for the comment content
        widgets = {
            'parent': forms.HiddenInput()  # Display the parent field as hidden
        }
