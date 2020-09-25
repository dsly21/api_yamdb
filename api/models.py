from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Reviews(models.Model):
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="reviews")

    def __str__(self):
        return self.text

"""     title = models.ForeignKey(
                                Title, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name="reviews") """

"""     title = models.ForeignKey(
                                Title, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name="comments")
    review = models.ForeignKey(
                                Title, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name="comments") """


class Comments(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="comments")

    def __str__(self):
        return self.text
