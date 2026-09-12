from django import forms
from django.forms import inlineformset_factory

from .models import News, Category, NewsInlineImage, Tag
from .tagging import get_or_create_tag
from .validators import validate_image_upload, validate_video_upload


def parse_keyword_names(raw: str) -> list[str]:
    names = []
    seen = set()
    for part in (raw or '').replace(';', ',').split(','):
        name = part.strip()
        if not name:
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        names.append(name[:80])
    return names


class NewsForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select select2', 'id': 'id_categories'}),
    )
    keywords = forms.CharField(
        required=False,
        label='Keywords / tags',
        help_text='Comma-separated keywords. Example: Climate, Diplomacy, Red Sea',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Climate, Diplomacy, Red Sea',
            'autocomplete': 'off',
        }),
    )

    class Meta:
        model = News
        fields = ['title', 'content', 'status', 'image', 'video', 'categories']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={
                'rows': 8,
                'class': 'form-control',
                'placeholder': 'Write your news content here. Use [inline:1] to place inline images by order number.',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the title',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            existing = list(self.instance.tags.values_list('name', flat=True))
            if existing and not self.data:
                self.fields['keywords'].initial = ', '.join(existing)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'content_type'):
            validate_image_upload(image)
        return image

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video and hasattr(video, 'content_type'):
            validate_video_upload(video)
        return video

    def clean_keywords(self):
        return parse_keyword_names(self.cleaned_data.get('keywords', ''))

    def apply_keywords(self, news: News) -> list[Tag]:
        names = self.cleaned_data.get('keywords') or []
        if not names:
            return list(news.tags.all())
        tags = [get_or_create_tag(name) for name in names]
        news.tags.set(tags)
        return tags


class NewsInlineImageForm(forms.ModelForm):
    class Meta:
        model = NewsInlineImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional caption'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'content_type'):
            validate_image_upload(image)
        return image


NewsInlineImageFormSet = inlineformset_factory(
    News,
    NewsInlineImage,
    form=NewsInlineImageForm,
    extra=2,
    can_delete=True,
)
