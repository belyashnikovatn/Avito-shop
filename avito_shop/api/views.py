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
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user is None:
                user = Profile.objects.create_user(
                    username=username, password=password)

            token = RefreshToken.for_user(user).access_token

            return Response({
                'token': str(token)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            serializer = BuySerializer(
                data=request.data,
                context={
                    'request': request,
                    'merch': slug
                }
            )
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendCoinSerializer(data=request.data)
        if serializer.is_valid():
            to_user = serializer.validated_data['toUser']
            amount = serializer.validated_data['amount']

            # Проверяем, существует ли получатель
            recipient = get_object_or_404(Profile, username=to_user)

            # Здесь добавить логику перевода монет

            return Response({"message": f"Sent {amount} coins to {to_user}"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
