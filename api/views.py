from django.core.mail import send_mail
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from .filters import TitleFilter
from .mixins import PaginationMixin, BasicCategoryGenreMixin
from .models import Category, Genre, Review, Title, User
from .permissions import (IsAdminOrReadOnly, CheckAuthorOrStaffPermission,
                          IsAdminPerm)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        CheckAuthorOrStaffPermission,
        IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('titles_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('titles_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        CheckAuthorOrStaffPermission,
        IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('reviews_id'))
        serializer.save(author=self.request.user)
        serializer.save(review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('reviews_id'))
        return review.comments.all()


@api_view(['POST'])
@permission_classes([AllowAny])
def send_email(request):
    """
    Функция для создания пользователя и отправки ему confirmation_code
    """
    email = request.POST.get('email')
    new_user = User.objects.create_user(email=email)
    conf_code = new_user.confirmation_code
    send_mail(
        'Ваш код подтверждения от Yamdb',
        f'Это ваш код подтверждения: {conf_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )
    return HttpResponse('Код подтверждения был отправлен на ваш email')


class CategoryView(BasicCategoryGenreMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreView(BasicCategoryGenreMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleView(PaginationMixin, viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def add_data(self, serializer):
        category = self.request.data.get('category', None)
        if category is not None:
            category = Category.objects.get(slug=category)
            serializer.save(category=category)
        genre = self.request.data.getlist('genre', None)
        if genre is not None:
            genre = Genre.objects.filter(slug__in=genre)
            serializer.save(genre=genre)
        serializer.save()

    def perform_create(self, serializer):
        self.add_data(serializer)

    def perform_update(self, serializer):
        self.add_data(serializer)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminPerm, permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }


def get_token(request):
    email = request.data.get('email')
    user = get_object_or_404(User, email=email)
    code = request.data.get('confirmation_code')
    if user.confirmation_code == code:
        tokens = get_tokens_for_user(user)
        return Response(tokens)
    return Response('неверный код подтверждения.')
