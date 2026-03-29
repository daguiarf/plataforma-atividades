from django.urls import path
from .views import LoginView, UserCreateView, UserListView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('', UserListView.as_view()),
    path('create/', UserCreateView.as_view()),
]