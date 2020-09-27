from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


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
    genre = models.ForeignKey(
        to=Genres,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Жанр',
        related_name='title',
    )
    year = models.PositiveIntegerField()


class Reviews(StrNameMixin, models.Model):
    text = models.TextField(max_length=500)
    score = models.PositiveIntegerField()
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="review"
    )
    title = models.ForeignKey(
                                Titles, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='произведение',
                                related_name="review")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)


class Comments(StrNameMixin, models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="comments"
    )
    title = models.ForeignKey(
                                Titles, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='произведение',
                                related_name="comment")
    review = models.ForeignKey(
                                Reviews, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='отзыв',
                                related_name="comment")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
