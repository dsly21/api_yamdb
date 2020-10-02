from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import serializers as ser

from .models import Comments, Reviews, User


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
    Переопределение сериалайзера для изменения названия полей
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
        data['token'] = str(refresh.access_token)
        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'email', 'role']

    def save(self, **kwargs):
        """
        При получении ключа 'role', изменение статусов is_staff, is_superuser
        """
        assert not hasattr(self, 'save_object'), (
            'Serializer `%s.%s` has old-style version 2 `.save_object()` '
            'that is no longer compatible with REST framework 3. '
            'Use the new-style `.create()` and `.update()` methods instead.' %
            (self.__class__.__module__, self.__class__.__name__)
        )

        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        if self.instance is not None:
            if 'role' in validated_data.keys():
                if validated_data['role'] == 'user':
                    self.instance.is_staff = False
                    self.instance.is_superuser = False
                elif validated_data['role'] == 'moderator':
                    self.instance.is_staff = True
                    self.instance.is_superuser = False
                elif validated_data['role'] == 'admin':
                    self.instance.is_staff = True
                    self.instance.is_superuser = True
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )
        return self.instance
