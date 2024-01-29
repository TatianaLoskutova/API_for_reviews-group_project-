from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import CustomUser

from .validators import validate_year
from .constants import MAX_LENGTH


class Category(models.Model):
    """
    Модель категорий.
    """

    name = models.CharField(
        'Название категории',
        max_length=MAX_LENGTH,
    )
    slug = models.SlugField(
        'Слаг категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель жанров.
    """

    name = models.CharField(
        'Название жанра',
        max_length=MAX_LENGTH,
    )
    slug = models.SlugField(
        'Слаг жанра',
        unique=True,
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Модель заголовков.
    """

    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH,
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles_cat',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание',
        max_length=MAX_LENGTH,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles_genre',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """
    Модель для заголовков жанров.
    """

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """
    Модель отзывов.
    """

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews_title',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        'Отзыв',
        max_length=MAX_LENGTH,
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        related_name='reviews_author',
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        error_messages={
            'validators': 'Оценка должна быть в диапазоне от 1 до 10!',
        }
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review',
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель комментариев.
    """

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments_review',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        'Комментарий',
        max_length=MAX_LENGTH,
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        related_name='comments_author',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
