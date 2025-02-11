
from django.contrib import admin
from django.urls import path
from api.views import AuthView, InfoView, SendCoinView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', AuthView.as_view(), name='auth'),
    path('api/info/', InfoView.as_view(), name='info'),
    path('api/sendCoin/', SendCoinView.as_view(), name='send-coin'),
]
