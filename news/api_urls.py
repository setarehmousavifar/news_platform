from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views
from .api import NewsViewSet, CategoryViewSet, CommentViewSet

router = DefaultRouter()
router.register('news', NewsViewSet, basename='api-v1-news')
router.register('categories', CategoryViewSet, basename='api-v1-categories')
router.register('comments', CommentViewSet, basename='api-v1-comments')

legacy_urlpatterns = [
    path('news/', views.news_list_api, name='news_list_api'),
    path('news/<int:pk>/', views.news_detail_api, name='news_detail_api'),
]

urlpatterns = [
    # OpenAPI schema & docs
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='api-redoc'),

    # v1 API
    path('v1/', include(router.urls)),
    path('v1/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('v1/auth/jwt/', TokenObtainPairView.as_view(), name='api_jwt_obtain'),
    path('v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name='api_jwt_refresh'),
] + legacy_urlpatterns
