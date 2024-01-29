from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from .mixins import MyModelViewSet
from reviews.models import Review, Category, Genre, Title
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSafeSerializer,
    TitleNotSafeSerializer,
    CategorySerializer,
    GenreSerializer
)
from .permissions import (
    IsAuthenticatedAuthorModeratoAdminOrReadOnly,
    IsAuthorOrReadOnly,
)
from .filters import TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для отзывов.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedAuthorModeratoAdminOrReadOnly,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews_title.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if partial is False:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    Представление для комментариев.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedAuthorModeratoAdminOrReadOnly,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments_review.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if partial is False:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class TitleViewSet(viewsets.ModelViewSet):
    """
    Представление для заголовков.
    """

    queryset = Title.objects.annotate(
        rating=Avg('reviews_title__score')
    ).all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSafeSerializer
        return TitleNotSafeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if partial is False:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class CategoryViewSet(MyModelViewSet):
    """
    Представление для категорий.
    """

    queryset = Category.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(MyModelViewSet):
    """
    Представление для жанров.
    """

    queryset = Genre.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
