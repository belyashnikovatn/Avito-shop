
from django.contrib import admin
from django.urls import path
from api.views import AuthView, ByeView, InfoView, SendCoinView, MerchViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', AuthView.as_view(), name='auth'),
    path('api/info/', InfoView.as_view(), name='info'),
    path('api/sendCoin/', SendCoinView.as_view(), name='send-coin'),
    path('api/buy/<slug:slug>/', ByeView.as_view(), name='bye'),
    path('api/merch/', MerchViewSet.as_view({'get': 'list'}), name='merch'),
]
