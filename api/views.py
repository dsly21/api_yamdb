from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .models import Reviews, Comments  #Title
from .serializers import ReviewSerializer, CommentSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

"""     def perform_create(self, serializer):
        get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user) """


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

"""     def perform_create(self, serializer):
        get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user) """
