from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes = serializers.SerializerMethodField()
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'published_date',
            'updated_at',
            'author',
            'likes',
            'views_count',
            'status',
            'categories',
        ]

    def get_likes(self, obj):
        return obj.total_likes()
