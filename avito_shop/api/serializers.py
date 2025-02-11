from rest_framework import serializers


class AuthRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class AuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class SendCoinSerializer(serializers.Serializer):
    toUser = serializers.CharField(max_length=150)
    amount = serializers.IntegerField(min_value=1)
