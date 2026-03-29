from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from core.utils.response import success_response
from core.swagger.decorators import publico_endpoint, api_schema

from .models import User
from .serializers import UserSerializer
from .jwt_serializers import CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @publico_endpoint(
        summary="Login",
        description="Autenticação via JWT",
        request=None,
        tags=["Auth"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @api_schema(
        summary="Criar usuário",
        description="Criação de usuário (admin)",
        request=UserSerializer,
        response=UserSerializer,
        tags=["User"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            success_response(serializer.data, "Usuário criado com sucesso"),
            status=status.HTTP_201_CREATED
        )


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @api_schema(
        summary="Listar usuários",
        description="Lista todos usuários (admin)",
        response=UserSerializer,
        tags=["User"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)