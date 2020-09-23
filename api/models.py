from django.db import models


class Reviews(models.Model):
    text = models.TextField()
    score = models.IntegerField()
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="reviews")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              blank=True, null=True, related_name="reviews")

    def __str__(self):
        return self.text


class Comments(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
                                User, on_delete=models.CASCADE,
                                related_name="comments")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    title = models.ForeignKey(
                                Title, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name="comments")
    review = models.ForeignKey(
                                Title, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name="comments")

    def __str__(self):
        return self.text
