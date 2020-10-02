import django_filters
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .filters import TitleFilter
from .mixins import PaginationMixin
from .models import Category, Comments, Genre, Reviews, Title, User
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserTokenSerializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('titles_id'))
        return title.reviews

    # чтобы проверить создание отзыва нужна аутентификация
    def perform_create(self, serializer):
        get_object_or_404(Titles, id=self.kwargs.get('titles_id'))
        serializer.save(author=self.request.user) # username


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    # чтобы проверить создание коммента нужна аутентификация
    def perform_create(self, serializer):
        get_object_or_404(Reviews, id=self.kwargs.get('reviews_id'))
        serializer.save(author=self.request.user) # username

    def get_queryset(self):
        review = get_object_or_404(Reviews, id=self.kwargs.get('reviews_id'))
        return review.comments




class TokenGetView(TokenObtainPairView):
    serializer_class = UserTokenSerializer


def send_email(request):
    """
    Функция для создания пользователя и отправки ему confirmation_code
    """
    email = request.GET.get('email')
    new_user = User.objects.create_user(email=email)
    conf_code = new_user.confirmation_code
    send_mail(
            'Confirmation code from Yamdb',
            f'This is your confirmation code: {conf_code}',
            from_email='from@yamdb.ru',
            recipient_list=[email]
        )
    return HttpResponse('Your confirmation code was sent to your email')


class CategoryView(
    PaginationMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('slug', 'name')
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly, )


class GenreView(
    PaginationMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class TitleView(PaginationMixin, viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        title = Title.objects.create(
            name=request.data['name'],
            year=request.data.get('year', None),
            description=request.data.get('description', None),
            rating=request.data.get('rating', None),
            category=Category.objects.get(slug=request.data.get('category'))
        )
        genres = Genre.objects.filter(slug__in=request.data.getlist('genre'))
        title.genre.add(*genres)
        serializer = TitleSerializer(title)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        super().update(self, request, *args, **kwargs)
