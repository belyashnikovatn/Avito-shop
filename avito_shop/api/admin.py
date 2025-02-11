from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin users."""

    list_display = ('username', 'coins',)
    search_fields = ('username',)
