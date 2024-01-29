from django.urls import path, include
from rest_framework.routers import DefaultRouter


from users.views import SignupAPI, CustomUserTokenAPI, UserViewSet

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

url_auth = [
    path('signup/', SignupAPI.as_view(), name='signup'),
    path('token/', CustomUserTokenAPI.as_view(), name='token'),
]

url_list = [
    path('', include(router.urls)),
    path('auth/', include(url_auth))
]

urlpatterns = [
    path('v1/', include(url_list)),
]
