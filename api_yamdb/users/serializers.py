from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.validators import UniqueValidator

from .models import CustomUser
from .constants import MAX_FOR_EMAIL, MIN_FOR_EMAIL, MAX_FOR_USERNAME


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    email = serializers.EmailField(
        validators=[
            MaxLengthValidator(
                MAX_FOR_EMAIL,
                'Email не должен превышать 254 символа'
            ),
            MinLengthValidator(MIN_FOR_EMAIL, 'Email не должен быть пустым'),
        ]
    )
    username = serializers.CharField(
        max_length=MAX_FOR_USERNAME,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя должно содержать только буквы, '
                        'цифры и символы: @ . + -',
            ),
        ]
    )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if CustomUser.objects.filter(email=email).exists()\
                and not CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует',
            )
        if CustomUser.objects.filter(username=username).exists() \
                and not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует',
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"!',
            )
        return data

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomUserSignupTokenSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения токена.
    """

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        confirmation_code = data.get('confirmation_code')
        username = data.get('username')

        if not CustomUser.objects.filter(username=username).exists():
            raise NotFound('User not found')
        if not CustomUser.objects.filter(
                confirmation_code=confirmation_code
        ).exists():
            raise ValidationError('Confirmation code not found')

        return data

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code', 'role')


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для юзера.
    """

    username = serializers.CharField(
        max_length=MAX_FOR_USERNAME,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message='Пользователь с таким именем уже существует!',
            ),
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя должно содержать только буквы, '
                        'цифры и символы: @ . + -',
            ),
        ]
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
