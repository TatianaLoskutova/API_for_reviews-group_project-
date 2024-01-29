from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.viewsets import GenericViewSet


class MyModelViewSet(CreateModelMixin, ListModelMixin,
                     DestroyModelMixin, GenericViewSet):
    """
    Класс представления для модели MyModel.
    Предоставляет возможность создания, просмотра списка, удаления
    и общего представления для модели MyModel.
    """

    pass
