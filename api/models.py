from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Reviews(models.Model):
    text = models.TextField()
    score = models.IntegerField()
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="reviews")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text


class Comments(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="comments")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text
