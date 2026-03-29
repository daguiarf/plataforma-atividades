from rest_framework import generics, status
from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.response import Response

from core.utils.response import success_response
from core.swagger.decorators import api_schema

from .models import Turma
from .serializers import TurmaSerializer

# permissão customizada
class IsAdminOrProfessorReadOnly(BasePermission):
    """
    - admin: full access
    - professor: somente GET
    """
    def has_permission(self, request, view):
        user = request.user
        # admin pode tudo
        if user.is_staff:
            return True
        # professor: só GET, HEAD, OPTIONS
        if getattr(user, "role", None) == "PROFESSOR" and request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return False


# apenas admin pode criar turmas
class TurmaCreateView(generics.CreateAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [IsAdminUser]

    @api_schema(
        summary="Criar turma",
        description="Criação de turma (apenas admin)",
        request=TurmaSerializer,
        response=TurmaSerializer,
        tags=["Turma"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            success_response(serializer.data, "Turma criada com sucesso"),
            status=status.HTTP_201_CREATED
        )


class TurmaListView(generics.ListAPIView):
    serializer_class = TurmaSerializer
    permission_classes = [IsAdminOrProfessorReadOnly]

    @api_schema(
        summary="Listar turmas",
        description="Lista todas as turmas (admin ou professor). Professores veem apenas suas turmas.",
        response=TurmaSerializer,
        tags=["Turma"],
    )
    def get_queryset(self):
        user = self.request.user
        # admin vê todas as turmas
        if user.is_staff:
            return Turma.objects.all()
        # professores: apenas suas turmas
        return Turma.objects.filter(professores=user)