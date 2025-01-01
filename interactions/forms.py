from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']  # فیلدهای فرم شامل متن نظر و نظر والد
        labels = {'content': 'متن نظر'}  # برچسب برای متن نظر
        widgets = {
            'parent': forms.HiddenInput()  # نمایش فیلد parent به صورت مخفی
        }
