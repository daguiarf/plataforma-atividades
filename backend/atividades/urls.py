from django.urls import path
from .views import (
    CriarAtividadeView,
    MinhasAtividadesView,
    AtualizarAtividadeView,
)

urlpatterns = [
    path('', CriarAtividadeView.as_view()),
    path('me/', MinhasAtividadesView.as_view()),
    path('<int:pk>/', AtualizarAtividadeView.as_view()),
]