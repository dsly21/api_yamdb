from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import serializers as ser

from .models import Category, Comment, Genre, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    def validate(self, attrs):
        title = self.context["view"].kwargs.get("titles_id")
        author = self.context["request"].user
        request_method = self.context["request"].method
        message = 'Author review already exist'
        if request_method == "POST":
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(message)
        return attrs

    class Meta:
        fields = ('__all__')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('__all__')
        model = Comment


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
        self.user = User.objects.filter(
            email=attrs[self.username_field]).first()

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.confirmation_code == attrs['confirmation_code']:
                raise ValidationError('Incorrect credentials.')

        if self.user is None or not self.user.is_active:
            raise ValidationError(
                                    'No active account found ',
                                    'with the given credentials')

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
    # многое непонятно в rating
    rating = serializers.DecimalField(read_only=True, max_digits=10,
                                      decimal_places=1, coerce_to_string=False)

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = [
                    'first_name',
                    'last_name',
                    'username',
                    'bio',
                    'email',
                    'role']
