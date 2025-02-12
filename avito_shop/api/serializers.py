from rest_framework import serializers
from django.shortcuts import get_list_or_404, get_object_or_404

from api.models import Gift, Buy, Profile, Merch


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class BuySerializer(serializers.Serializer):

    def validate(self, data):
        """
        Проверка:
        - наличие объектов мерч и пользователь
        - достаточного количества монет у пользователя.
        """
        user = self.context['request'].user
        merch = self.context.get('merch')

        merch = get_object_or_404(Merch, name=merch)
        user = get_object_or_404(Profile, username=user)

        if user.coins < merch.price:
            raise serializers.ValidationError(
                {'error': 'Недостаточно монет для покупки.'})

        return data


class SendCoinSerializer(serializers.Serializer):

    def validate(self, data):
        """
        Проверка:
        - наличие объектов пользователи, количество
        - количества: целое число, больше 0
        - достаточного количества монет у пользователя
        - польозователь не сам он.
        """
        from_user = self.context['request'].user
        to_user = self.context.get('to_user')
        amount = self.context.get('amount')

        from_user = get_object_or_404(Profile, username=from_user)
        to_user = get_object_or_404(Profile, username=to_user)

        if to_user == from_user:
            raise serializers.ValidationError(
                {'error': 'Нельзя переводить деньги себе.'})

        if amount is None:
            raise serializers.ValidationError(
                {'error': 'Укажите количество.'})

        if not to_user:
            raise serializers.ValidationError(
                {'error': 'Укажите пользователя.'})

        if not isinstance(amount, int):
            raise serializers.ValidationError(
                {'error': 'Это не целое число.'})

        if amount <= 0:
            raise serializers.ValidationError(
                {'error': 'Перевод должен быть больше 0.'})

        if from_user.coins < amount:
            raise serializers.ValidationError(
                {'error': 'Недостаточно монет для передачи.'})

        return data


class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merch
        fields = ('__all__')
