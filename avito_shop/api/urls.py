from django.urls import path

from api.views import (
    AuthView,
    ByeView,
    InfoViewSet,
    MerchViewSet,
    SendCoinView,
)


app_name = 'api'

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),
    path('info/', InfoViewSet.as_view({'get': 'list'}), name='info'),
    path('merch/', MerchViewSet.as_view({'get': 'list'}), name='merch'),
    path('sendCoin/', SendCoinView.as_view(), name='send-coin'),
    path('buy/<slug:slug>/', ByeView.as_view(), name='bye'),
]