from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from api.serializers import (
    AuthSerializer,
    BuySerializer,
    SendCoinSerializer,
)
from api.models import Profile, Gift, Buy, Merch


class AuthView(APIView):
    """
    Аутентификация и получение JWT-токена.
    При первой аутентификации
    пользователь создается автоматически.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # проверка данных
            serializer = AuthSerializer(data=request.data)

            # основная логика представления
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']

                user = authenticate(username=username, password=password)

                if user is None:
                    user = Profile.objects.create_user(
                        username=username, password=password)

                token = RefreshToken.for_user(user).access_token

                return Response({
                    'description': 'Успешная аутентификация.',
                    'JWT-токен для доступа к защищенным ресурсам.': str(token),
                }, status=status.HTTP_200_OK)

            return Response(
                {'description': 'Неверный запрос.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {'description': f'Внутренняя ошибка сервера: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'user': str(self.request.user),
        })


class ByeView(APIView):
    """Купить предмет за монеты."""
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            # проверка данных
            serializer = BuySerializer(
                data=request.data,
                context={
                    'request': request,
                    'merch': slug
                }
            )

            # основная логика представления
            if serializer.is_valid():
                user = Profile.objects.get(username=request.user)
                merch = Merch.objects.get(name=slug)

                user.coins -= merch.price
                user.save()
                Buy.objects.create(user=user, merch=merch)
                return Response(
                    {'description': 'Успешный ответ.'},
                    status=status.HTTP_200_OK
                )

            return Response(
                {'description': 'Неверный запрос.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {'description': f'Внутренняя ошибка сервера: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SendCoinView(APIView):
    """Отправить монеты другому пользователю."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # проверка данных
            serializer = SendCoinSerializer(
                data=request.data,
                context={
                    'request': request,
                    'to_user': request.data.get('toUser'),
                    'amount': request.data.get('amount')
                }
            )
            # основная логика представления
            if serializer.is_valid():
                from_user = Profile.objects.get(username=request.user)
                to_user = Profile.objects.get(
                    username=request.data['toUser'])
                amount = request.data['amount']

                from_user.coins -= amount
                from_user.save()
                to_user.coins += amount
                to_user.save()
                Gift.objects.create(
                    from_user=from_user,
                    to_user=to_user,
                    amount=amount)
                return Response(
                    {'description': 'Успешный ответ.'},
                    status=status.HTTP_200_OK
                )

            return Response(
                {'description': 'Неверный запрос.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {'description': f'Внутренняя ошибка сервера: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
