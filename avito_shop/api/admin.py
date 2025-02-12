from django.contrib import admin
from django.contrib.auth import get_user_model

from api.models import Buy, Gift, Merch
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin users."""

    list_display = ('username', 'coins',)
    search_fields = ('username',)


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    """Admin Buy"""


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    """Admin Gift"""


@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    """Admin Merch"""
