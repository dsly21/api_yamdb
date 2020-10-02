from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt import serializers as ser

from .models import Category, Comments, Genre, Reviews, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('__all__')
        model = Reviews


class CommentSerializer(serializers.ModelSerializer):
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

    def __init__(self, *args, **kwargs):

        super(UserTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields.pop('password', None)
        self.fields['confirmation_code'] = ser.PasswordField()

    def _validate(self, attrs):
        self.user = User.objects.filter(email=attrs[self.username_field]).first()

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.confirmation_code == attrs['confirmation_code']:
                raise ValidationError('Incorrect credentials.')

        if self.user is None or not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')

        return {}

    def validate(self, attrs):
        data = self._validate(attrs)

        refresh = self.get_token(self.user)

        # data['refresh'] = str(refresh)
        data['token'] = str(refresh.access_token)

        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
