from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Создание кастомной модели пользователя с confirmation code
    """

    def create_user(self, email, **extra_fields):
        """
        Создание User через email
        """
        if not email:
            raise ValueError('Укажите email, пожалуйста.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        password = self.make_random_password()
        confirmation_code = self.make_random_password()
        user.set_password(password)
        user.confirmation_code = confirmation_code
        user.save()
        return user

    def create_superuser(self, email, **extra_fields):
        """
        Создание SuperUser через email.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')
        return self.create_user(email, **extra_fields)
