from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from core.pagination import CustomPagination
from core.utils.response import success_response
from core.swagger.decorators import aluno_endpoint, professor_endpoint

from users.permissions import IsProfessor, IsAluno
from atividades.models import Atividade
from .models import Resposta
from .serializers import RespostaSerializer


class CriarRespostaView(generics.CreateAPIView):
    queryset = Resposta.objects.all()
    serializer_class = RespostaSerializer
    permission_classes = [IsAuthenticated, IsAluno]

    @aluno_endpoint(
        summary="Enviar resposta",
        description="Aluno envia resposta para uma atividade. Só pode enviar uma vez.",
        request=RespostaSerializer,
        response=RespostaSerializer,
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(aluno=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            success_response(serializer.data, "Resposta enviada com sucesso"),
            status=status.HTTP_201_CREATED
        )


class AtualizarRespostaView(generics.UpdateAPIView):
    serializer_class = RespostaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ALUNO":
            return Resposta.objects.filter(aluno=user)

        if user.role == "PROFESSOR":
            return Resposta.objects.filter(atividade__professor=user)

        return Resposta.objects.none()

    @extend_schema(
        summary="Atualizar resposta",
        description="""
        ALUNO: pode editar sua resposta antes da data limite  
        PROFESSOR: pode corrigir (nota e feedback)
        """,
        request=RespostaSerializer,
        responses={200: RespostaSerializer},
        tags=["Resposta"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(
            success_response(serializer.data, "Resposta atualizada com sucesso"),
            status=status.HTTP_200_OK
        )


class MinhasRespostasView(APIView):
    permission_classes = [IsAuthenticated, IsAluno]

    @aluno_endpoint(
        summary="Listar minhas respostas",
        description="Lista respostas enviadas pelo aluno",
        response=RespostaSerializer,
    )
    def get(self, request):
        user = request.user

        if not user.turma:
            return Response(
                {"success": False, "message": "Aluno sem turma"},
                status=400
            )

        queryset = Resposta.objects.filter(
            aluno=user
        ).select_related("atividade")

        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = RespostaSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class RespostasPorAtividadeView(APIView):
    permission_classes = [IsAuthenticated]

    @professor_endpoint(
        summary="Listar respostas da atividade",
        description="""
        Retorna respostas de uma atividade conforme o tipo de usuário:

        PROFESSOR:
        - Lista TODAS as respostas dos alunos
        - Apenas se for o criador da atividade

        ALUNO:
        - Retorna APENAS sua própria resposta
        - Apenas se a atividade for da sua turma

        - Professor não acessa atividade de outro professor
        - Aluno não acessa atividade de outra turma
        - Aluno nunca vê resposta de outros alunos
        """,
        response=RespostaSerializer,
        tags=["Respostas"],
    )
    def get(self, request, atividade_id):
        user = request.user

        try:
            atividade = Atividade.objects.select_related("professor", "turma").get(id=atividade_id)
        except Atividade.DoesNotExist:
            raise NotFound("Atividade não encontrada")

        if user.role == "PROFESSOR":
            if atividade.professor != user:
                raise PermissionDenied("Você não pode acessar respostas dessa atividade")

            queryset = Resposta.objects.filter(
                atividade=atividade
            ).select_related("aluno")

        elif user.role == "ALUNO":
            if not user.turma:
                raise PermissionDenied("Aluno sem turma")

            if atividade.turma_id != user.turma_id:
                raise PermissionDenied("Você não pode acessar essa atividade")

            queryset = Resposta.objects.filter(
                atividade=atividade,
                aluno=user
            ).select_related("aluno")

        else:
            raise PermissionDenied("Role inválida")

        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = RespostaSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)