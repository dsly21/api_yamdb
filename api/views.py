from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from rest_framework import generics, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Comments, Reviews, User  # Title
from .serializers import (CommentSerializer, ReviewSerializer, UserSerializer,
                          UserTokenSerializer)


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
    filter_backends = [rest_framework.DjangoFilterBackend]
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


class UserMeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]

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
