from django.contrib.auth import authenticate
from rest_framework_simplejwt import exceptions
from rest_framework import serializers
from rest_framework.fields import EmailField
from rest_framework_simplejwt import serializers as ser

from .models import Reviews, Comments


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('__all__')
        model = Reviews


class CommentSerializer(serializers.Serializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('__all__')
        model = Comments


class UserTokenSerializer(ser.TokenObtainPairSerializer):
    """
    Пытаюсь переопределить названия полей для получения токена!!!
    """

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['email'] = EmailField(allow_blank=False)
    #     # self.fields['confirmation_code'] = ser.PasswordField()

    def _validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    def validate(self, attrs):
        data = self._validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
