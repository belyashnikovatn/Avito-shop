from rest_framework import serializers
from django.shortcuts import get_list_or_404, get_object_or_404

from api.models import Gift, Buy, Profile, Merch


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class BuySerializer(serializers.Serializer):

    def validate(self, data):
        """Проверка достаточного количества монет у пользователя."""
        user = self.context['request'].user
        merch = self.context.get('merch')

        merch = get_object_or_404(Merch, name=merch)
        user = get_object_or_404(Profile, username=user)

        if user.coins < merch.price:
            raise serializers.ValidationError(
                {'error': 'Недостаточно монет для покупки.'})

        return data

    def create(self, validated_data):
        """Создание покупки и списание монет у пользователя."""
        user = self.context['request'].user
        merch = get_object_or_404(Merch, name=validated_data.get('merch'))

        user.coins -= merch.price
        user.save()
        return Buy.objects.create(user=user, merch=merch)


class SendCoinSerializer(serializers.Serializer):
    toUser = serializers.CharField(max_length=150)
    amount = serializers.IntegerField(min_value=1)
