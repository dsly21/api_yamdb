from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
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
    rating = serializers.DecimalField(read_only=True, max_digits=10,
                                      decimal_places=1, coerce_to_string=False)

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'bio',
                  'email',
                  'role']
