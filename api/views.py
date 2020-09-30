from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Reviews, User, Titles # Comments
from .serializers import ReviewSerializer, CommentSerializer, UserTokenSerializer


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
