from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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


class Category(models.Model):
    name = models.CharField(max_length=75, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id', )

    def __str__(self):
        return f'<Категория: {self.name}>'


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id', )

    def __str__(self):
        return f'<Жанр: {self.name}>'


class Title(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Название', blank=False
    )
    year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Год выпуска',
        validators=[MaxValueValidator(datetime.now().year)],
        db_index=True,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles',
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

    def __str__(self):
        return f'<Произведение: {self.name}>'


class Review(models.Model):
    text = models.TextField(verbose_name="текст")
    score = models.PositiveIntegerField(
        verbose_name="Оценка",
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
                                    db_index=True)

    def __str__(self):
        return f'<Отзыв: {self.name}>'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(models.Model):
    text = models.TextField(verbose_name="текст")
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="comments",
                                verbose_name="автор")

    review = models.ForeignKey(
                                Review, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='отзыв',
                                related_name="comments")

    pub_date = models.DateTimeField(
                                    "Дата публикации",
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return f'<Комментарий: {self.name}>'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
