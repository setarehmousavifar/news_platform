from django import forms
from django.contrib import admin

from .forms import parse_keyword_names
from .models import News, Category, Tag
from .tagging import get_or_create_tag


class NewsAdminForm(forms.ModelForm):
    keywords = forms.CharField(
        required=False,
        label='Add keywords',
        help_text=(
            'Type new keywords separated by commas (e.g. Climate, Diplomacy). '
            'They are created automatically and selected for this story. '
            'You can also pick existing tags from the box below.'
        ),
        widget=forms.TextInput(attrs={
            'style': 'width: 100%; max-width: 42rem;',
            'placeholder': 'Climate, Diplomacy, Red Sea',
        }),
    )

    class Meta:
        model = News
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and not self.data:
            names = list(self.instance.tags.values_list('name', flat=True))
            if names:
                self.fields['keywords'].initial = ', '.join(names)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'author', 'get_categories', 'get_tags', 'published_date', 'status')
    search_fields = ('title', 'content', 'tags__name')
    list_filter = ('author', 'status', 'categories', 'tags')
    filter_horizontal = ('categories', 'tags')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'author', 'status'),
        }),
        ('Media', {
            'fields': ('image', 'video', 'video_url'),
        }),
        ('Topics & keywords', {
            'fields': ('categories', 'keywords', 'tags'),
            'description': (
                'Use “Add keywords” for quick comma-separated tags, '
                'or choose existing tags in the filter box.'
            ),
        }),
        ('Stats', {
            'fields': ('views_count',),
            'classes': ('collapse',),
        }),
    )

    def get_categories(self, obj):
        return ', '.join(category.name for category in obj.categories.all()) or '—'
    get_categories.short_description = 'Categories'

    def get_tags(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all()[:8]) or '—'
    get_tags.short_description = 'Keywords'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        keyword_names = parse_keyword_names(form.cleaned_data.get('keywords', ''))
        if not keyword_names:
            return
        news = form.instance
        selected = list(news.tags.all())
        created = [get_or_create_tag(name) for name in keyword_names]
        by_id = {tag.pk: tag for tag in [*selected, *created]}
        news.tags.set(list(by_id.values()))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
