from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Count, Exists, OuterRef, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view, extend_schema_field
from drf_spectacular.types import OpenApiTypes

from accounts.permissions import ReadOnlyOrAdmin, IsAuthorOrSuperAdmin, can_edit_news
from interactions.models import Comment, Like
from interactions.services import toggle_news_like, toggle_comment_like
from .filters import NewsFilter
from .models import News, Category
from .validators import validate_image_upload, validate_video_upload
from . import services


def _as_drf_validation(exc):
    if hasattr(exc, 'messages'):
        return ValidationError(list(exc.messages))
    return ValidationError(str(exc))


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    like_total = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'news', 'user', 'content', 'parent',
            'created_at', 'replies', 'like_total',
        ]
        read_only_fields = ['user', 'created_at']

    def validate_content(self, value):
        value = (value or '').strip()
        if len(value) < 2:
            raise ValidationError('Comment must be at least 2 characters.')
        if len(value) > 2000:
            raise ValidationError('Comment must be at most 2000 characters.')
        return value

    def validate(self, attrs):
        news = attrs.get('news') or getattr(self.instance, 'news', None)
        parent = attrs.get('parent')
        if news and news.status != News.Status.PUBLISHED:
            raise ValidationError({'news': 'Comments are only allowed on published news.'})
        if parent:
            if news and parent.news_id != news.id:
                raise ValidationError({'parent': 'Parent comment must belong to the same news.'})
            if parent.parent_id is not None:
                raise ValidationError({'parent': 'Only one-level replies are allowed.'})
        return attrs

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_replies(self, obj):
        if obj.parent_id:
            return []
        qs = obj.replies.all()
        return CommentSerializer(qs, many=True, context=self.context).data

    @extend_schema_field(OpenApiTypes.INT)
    def get_like_total(self, obj):
        if hasattr(obj, 'like_total'):
            return obj.like_total
        return obj.likes.filter(is_like=True).count()


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )

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
            'author_id',
            'author_username',
            'likes',
            'user_has_liked',
            'views_count',
            'status',
            'categories',
            'image',
            'video',
        ]
        read_only_fields = [
            'slug', 'published_date', 'updated_at', 'views_count',
            'author', 'author_id', 'author_username',
        ]

    def validate_image(self, image):
        if image and hasattr(image, 'content_type'):
            try:
                validate_image_upload(image)
            except DjangoValidationError as exc:
                raise _as_drf_validation(exc)
        return image

    def validate_video(self, video):
        if video and hasattr(video, 'content_type'):
            try:
                validate_video_upload(video)
            except DjangoValidationError as exc:
                raise _as_drf_validation(exc)
        return video

    def validate_status(self, value):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.user_type in ('admin', 'super_admin'):
            return value
        return News.Status.PUBLISHED

    @extend_schema_field(OpenApiTypes.INT)
    def get_likes(self, obj):
        if hasattr(obj, 'like_count'):
            return obj.like_count
        return obj.total_likes()

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if hasattr(obj, 'user_has_liked'):
            return bool(obj.user_has_liked)
        return obj.liked_by.filter(user=request.user).exists()


@extend_schema_view(
    list=extend_schema(summary='List news', tags=['News']),
    retrieve=extend_schema(summary='Retrieve news by slug', tags=['News']),
    create=extend_schema(summary='Create news (admin)', tags=['News']),
    update=extend_schema(summary='Update news (author/super_admin)', tags=['News']),
    partial_update=extend_schema(summary='Partial update news', tags=['News']),
    destroy=extend_schema(summary='Soft-delete news', tags=['News']),
)
class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [ReadOnlyOrAdmin, IsAuthorOrSuperAdmin]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsFilter
    search_fields = ['title', 'content']
    ordering_fields = ['published_date', 'views_count', 'title']
    ordering = ['-published_date']

    def get_queryset(self):
        user = self.request.user
        qs = (
            News.objects.all()
            .select_related('author')
            .prefetch_related('categories')
            .annotate(like_count=Count('liked_by', distinct=True))
        )
        if user.is_authenticated:
            qs = qs.annotate(
                user_has_liked=Exists(
                    Like.objects.filter(news_id=OuterRef('pk'), user=user)
                )
            )
        if not (user.is_authenticated and user.user_type in ('admin', 'super_admin')):
            qs = qs.filter(status=News.Status.PUBLISHED)
        return qs.order_by('-published_date')

    def perform_create(self, serializer):
        status_value = serializer.validated_data.get('status', News.Status.PUBLISHED)
        serializer.save(author=self.request.user, status=status_value)

    def perform_update(self, serializer):
        news = self.get_object()
        if not can_edit_news(self.request.user, news):
            raise PermissionDenied('You cannot edit this news item.')
        serializer.save()

    def perform_destroy(self, instance):
        services.soft_delete_news(instance)

    @extend_schema(summary='Toggle like on news', tags=['News'])
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        news = self.get_object()
        if news.status != News.Status.PUBLISHED:
            raise PermissionDenied('Only published news can be liked.')
        liked, total = toggle_news_like(request.user, news)
        return Response({'liked': liked, 'total_likes': total})


@extend_schema_view(
    list=extend_schema(summary='List categories', tags=['Categories']),
    retrieve=extend_schema(summary='Retrieve category', tags=['Categories']),
)
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']


@extend_schema_view(
    list=extend_schema(summary='List comments', tags=['Comments']),
    retrieve=extend_schema(summary='Retrieve comment', tags=['Comments']),
    create=extend_schema(summary='Create comment (authenticated)', tags=['Comments']),
    destroy=extend_schema(summary='Delete own comment', tags=['Comments']),
)
class CommentViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['news', 'parent']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = (
            Comment.objects.select_related('user', 'news')
            .prefetch_related('replies__user', 'likes')
            .annotate(like_total=Count('likes', filter=Q(likes__is_like=True)))
            .order_by('-created_at')
        )
        if self.action == 'list' and 'parent' not in self.request.query_params:
            qs = qs.filter(parent=None)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.user_id != user.id and user.user_type != 'super_admin':
            raise PermissionDenied('You can only delete your own comments.')
        instance.delete()

    @extend_schema(summary='Toggle like on comment', tags=['Comments'])
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        is_like = str(request.data.get('is_like', '1')) != '0'
        result = toggle_comment_like(request.user, comment, is_like=is_like)
        return Response(result)
