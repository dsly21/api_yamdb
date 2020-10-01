import django_filters
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Reviews, Comments, User, Titles
from .serializers import ReviewSerializer, CommentSerializer, UserTokenSerializer, UserSerializer


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

    def get_queryset(self):
        review = get_object_or_404(Reviews, id=self.kwargs.get('reviews_id'))
        return review.comments

    # чтобы проверить создание коммента нужна аутентификация
    def perform_create(self, serializer):
        get_object_or_404(Reviews, id=self.kwargs.get('reviews_id'))
        serializer.save(author=self.request.user) # username


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


class UsersViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['username',]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserMeView(generics.UpdateAPIView):
    queryset = User.objects.filter(id=1)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]
