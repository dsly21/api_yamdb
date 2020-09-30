from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy

from .managers import CustomUserManager


class User(AbstractUser):
    """
    Создание кастомной модели User для того, чтобы email был главным полем.
    """
    CHOICES = {
        ('AD', 'admin'),
        ('MD', 'moderator'),
        ('US', 'user')
    }

    username = models.CharField(max_length=50, unique=False, default='', blank=True)
    bio = models.CharField(max_length=2000)
    role = models.CharField(max_length=2, choices=CHOICES, default='user')
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    confirmation_code = models.CharField(max_length=200, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # для переопределения функций create_user, create_superuser
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class StrNameMixin():
    def __str__(self):
        return self.text


class Categories(StrNameMixin, models.Model):
    name = models.CharField(max_length=75)
    slug = models.SlugField()


class Genres(StrNameMixin, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()


class Titles(StrNameMixin, models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        to=Categories,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='title',
    )
    year = models.PositiveIntegerField()


class GenreTitle(models.Model):
    title = models.ForeignKey(
        to=Titles,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Произведение',
        related_name='title'
    )
    genre = models.ForeignKey(
        to=Genres,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Жанр',
        related_name='genre'
    )


class Reviews(StrNameMixin, models.Model):
    text = models.TextField(max_length=500)
    score = models.PositiveIntegerField() # дописать range значений
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="reviews"
    )
    title = models.ForeignKey(
                                Titles, on_delete=models.CASCADE,
                                blank=True, null=True,
                                verbose_name='произведение',
                                related_name="reviews")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)


class Comments(StrNameMixin, models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="comments"
    )
    review = models.ForeignKey(
                                Reviews, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='отзыв',
                                related_name="comments")

    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
