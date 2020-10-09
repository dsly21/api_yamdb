from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy
from django.core.validators import MaxValueValidator, MinValueValidator

from .managers import CustomUserManager


class User(AbstractUser):
    """
    Создание кастомной модели User для того, чтобы email был главным полем.
    """
    CHOICES = {
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user')
    }

    username = models.CharField(max_length=50, unique=True, blank=True)
    bio = models.TextField(max_length=2000, blank=True)
    role = models.CharField(max_length=10, choices=CHOICES, default='user')
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    confirmation_code = models.CharField(max_length=200, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # для переопределения функций create_user, create_superuser
    objects = CustomUserManager()


class StrNameMixin():
    def __str__(self):
        return self.text


class Category(StrNameMixin, models.Model):
    name = models.CharField(max_length=75, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id', )


class Genre(StrNameMixin, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('id', )


class Title(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Название', blank=False
    )
    year = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Год выпуска'
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='title',
    )
    description = models.TextField(
        blank=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        to=Genre, verbose_name='Жанр', related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(StrNameMixin, models.Model):
    text = models.TextField(verbose_name="текст")
    score = models.PositiveIntegerField(verbose_name="оценка",
                                        validators=[
                                            MinValueValidator(1, message="Минимальная оценка - 1"),
                                            MaxValueValidator(10, message="Максимальная оценка - 10")])
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="reviews",
                                verbose_name="автор"
    )
    title = models.ForeignKey(
                                Title, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='произведение',
                                related_name="reviews")
    pub_date = models.DateTimeField(
                                    "Дата публикации",
                                    auto_now_add=True,
                                    db_index=True) # нужен ли тут verbose?

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Отзыв"


class Comment(models.Model):
    text = models.TextField(verbose_name="текст")
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="comments",
                                verbose_name="автор"
    )

    review = models.ForeignKey(
                                Review, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='отзыв',
                                related_name="comments")

    pub_date = models.DateTimeField(
                                    "Дата публикации",
                                    auto_now_add=True,
                                    db_index=True) # нужен ли тут verbose?

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
