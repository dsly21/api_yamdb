from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .managers import CustomUserManager


class User(AbstractUser):
    """
    Создание кастомной модели User для того, чтобы email был главным полем.
    """
    class Role(models.TextChoices):
        ADMIN = 'admin', 'admin'
        MODERATOR = 'moderator', 'moderator'
        USER = 'user', 'user'

    username = models.CharField(max_length=50, unique=True,
                                blank=True, verbose_name='Ник')
    bio = models.TextField(blank=True, verbose_name='Био')
    role = models.CharField(max_length=30, choices=Role.choices,
                            default=Role.USER, verbose_name='Роль')
    email = models.EmailField('email address', unique=True)
    confirmation_code = models.CharField(max_length=200, blank=True,
                                         verbose_name='Код подтверждения')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class StrNameMixin():
    def __str__(self):
        return self.text


class Category(StrNameMixin, models.Model):
    name = models.CharField(max_length=75)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('id', )


class Genre(StrNameMixin, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('id', )


class Title(StrNameMixin, models.Model):
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
        related_name='title',)
    description = models.CharField(
        max_length=255, blank=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        to=Genre, verbose_name='Жанр', related_name='title'
    )


class Review(StrNameMixin, models.Model):
    text = models.TextField(max_length=500)
    score = models.PositiveIntegerField(
                                        validators=[
                                            MinValueValidator(1),
                                            MaxValueValidator(10)])
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="reviews"
    )
    title = models.ForeignKey(
                                Title, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='произведение',
                                related_name="reviews")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)


class Comment(StrNameMixin, models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="comments"
    )

    review = models.ForeignKey(
                                Review, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='отзыв',
                                related_name="comments")

    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
