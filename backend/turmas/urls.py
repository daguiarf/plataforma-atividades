from django.urls import path
from .views import TurmaCreateView, TurmaListView

urlpatterns = [
    path('', TurmaListView.as_view()),
    path('create/', TurmaCreateView.as_view()),
]