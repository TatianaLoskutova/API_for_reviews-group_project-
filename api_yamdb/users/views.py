from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from .models import CustomUser
from .permissions import IsSuperUserOrAdmin
from .serializers import (
    CustomUserSignupTokenSerializer,
    UserSerializer,
    UserSignupSerializer
)
from .utils import generate_confirmation_code


def generate_jwt_token(user):
    """
    Функция для создания токена.
    """
    expiration_time = datetime.utcnow() + timedelta(days=7)

    payload = {
        'user_id': user.id,
        'exp': expiration_time,
        'iat': datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


class SignupAPI(APIView):
    """
    Представления для регистрации пользователя.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserSignupSerializer

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            role = request.data.get('role', CustomUser.Role.USER)

            if role not in [choice[0] for choice in
                            CustomUser.Role.choices]:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if CustomUser.objects.filter(
                email=email,
                username=username
            ).exists():
                return Response(serializer.data, status=status.HTTP_200_OK)

            confirmation_code = generate_confirmation_code(email)

            CustomUser.objects.create_user(
                email=email,
                username=username,
                confirmation_code=confirmation_code,
                role=role,
            )
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserTokenAPI(APIView):
    """
    Представление для получения токена.
    """

    serializer_class = CustomUserSignupTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CustomUserSignupTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        try:
            user = CustomUser.objects.get(
                username=username, confirmation_code=confirmation_code
            )
        except ValueError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        access_token = AccessToken.for_user(user)
        return Response(
            {'token': str(access_token)}, status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Представления для работы с пользователями.
    """

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username']

    def get_permissions(self):
        if self.action in (
            'list', 'retrieve', 'create', 'partial_update', 'destroy'
        ):
            permission_classes = [IsSuperUserOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(
        detail=False, methods=['get', 'patch', 'post', 'delete'], url_path='me'
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method in ['PATCH', 'POST']:
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid()\
                    and 'role' not in serializer.validated_data:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'DELETE':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if partial is False:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
