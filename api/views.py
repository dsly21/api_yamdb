from django.core.mail import send_mail
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (generics, permissions, status,
                            viewsets, views)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api_yamdb import settings
from .filters import TitleFilter
from .mixins import PaginationMixin, BasicCategoryGenreMixin
from .models import Category, Genre, Review, Title, User
from .permissions import IsAdminOrReadOnly, CheckAuthorOrStaffPermission
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


# def token_get(request, email, conf_code):
#     # serializer_class = TokenObtainSlidingSerializer
#     if request.method == 'POST':

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


class UsersViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        if username == 'me':
            return Response(
                data='Такое имя запрещено',
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
                User.objects.filter(email=email).exists() or
                User.objects.filter(username=username).exists()):
            return Response(
                serializer.validated_data,
                status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)


class UserMeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, username=self.kwargs['username'])
        self.check_object_permissions(self.request, obj)
        return obj


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }


@permission_classes([AllowAny])
class GetTokenView(APIView):

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        code = request.data.get('confirmation_code')
        if user.confirmation_code == code:
            tokens = get_tokens_for_user(user)
            return Response(tokens)
        return Response('неверный код подтверждения.')
