from django.urls import path
from .views import (
    CriarRespostaView,
    AtualizarRespostaView,
    MinhasRespostasView,
    RespostasPorAtividadeView,
)

urlpatterns = [
    path('', CriarRespostaView.as_view()),
    path('me/', MinhasRespostasView.as_view()),
    path('<int:pk>/', AtualizarRespostaView.as_view()),
    path('atividade/<int:atividade_id>/', RespostasPorAtividadeView.as_view()),
]