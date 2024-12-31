from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # فقط متن نظر
        labels = {'content': 'متن نظر'}  # برچسب فیلد
