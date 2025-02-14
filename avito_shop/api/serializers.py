from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Buy, Gift, Merch, Profile


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

        # user = get_object_or_404(Profile, username=user)
        try:
            user = Profile.objects.get(username=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Пользователь не найден.'},
            )
        try:
            merch = Merch.objects.get(name=merch)
        except Merch.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Мерч не найден.'},
            )
        # merch = get_object_or_404(Merch, name=merch)

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

        # from_user = get_object_or_404(Profile, username=from_user)
        try:
            from_user = Profile.objects.get(username=from_user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Пользователь не найден.'},
            )
        try:
            to_user = Profile.objects.get(username=to_user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Пользователь не найден.'},
            )
        # to_user = get_object_or_404(Profile, username=to_user)

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


class InventorySerializer(serializers.Serializer):
    type = serializers.CharField(source='merch__name')
    quantity = serializers.IntegerField()


class CoinHistoryReceivedSerializer(serializers.Serializer):
    fromUser = serializers.CharField(source='from_user.username')
    amount = serializers.IntegerField()


class CoinHistorySentSerializer(serializers.Serializer):
    toUser = serializers.CharField(source='to_user.username')
    amount = serializers.IntegerField()


class ProfileDetailSerializer(serializers.Serializer):
    coins = serializers.IntegerField()
    inventory = serializers.SerializerMethodField()
    coinHistory = serializers.SerializerMethodField()

    def get_inventory(self, obj):
        inventory = Buy.objects.filter(
            user=obj).values('merch__name').annotate(quantity=Count('merch'))
        return [{
            'type': item['merch__name'],
            'quantity': item['quantity']} for item in inventory]

    def get_coinHistory(self, obj):
        received = Gift.objects.filter(to_user=obj).values(
            'from_user__username').annotate(amount=Sum('amount'))
        sent = Gift.objects.filter(from_user=obj).values(
            'to_user__username').annotate(amount=Sum('amount'))

        return {
            'received': [
                {
                    'fromUser': item['from_user__username'],
                    'amount': item['amount']} for item in received
            ],
            'sent': [
                {
                    'toUser': item['to_user__username'],
                    'amount': item['amount']} for item in sent
            ]
        }
