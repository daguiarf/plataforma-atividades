from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from core.pagination import CustomPagination
from core.utils.response import success_response

from users.permissions import IsProfessor

from core.swagger.decorators import professor_endpoint, publico_endpoint

from .models import Atividade
from .serializers import AtividadeSerializer


class CriarAtividadeView(generics.CreateAPIView):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    @professor_endpoint(
        summary="Criar atividade",
        description="Cria uma nova atividade vinculada a uma turma. O professor precisa pertencer à turma.",
        request=AtividadeSerializer,
        response=AtividadeSerializer,
        tags=["Atividades"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        turma = serializer.validated_data.get("turma")
        user = self.request.user

        # valida se o professor pertence à turma
        if not turma.professores.filter(id=user.id).exists():
            raise PermissionDenied("Você não pertence a essa turma")

        serializer.save(professor=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            success_response(serializer.data, "Atividade criada com sucesso"),
            status=status.HTTP_201_CREATED
        )


class AtualizarAtividadeView(generics.UpdateAPIView):
    serializer_class = AtividadeSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_queryset(self):
        # professor só pode editar/deletar atividades que criou
        return Atividade.objects.filter(professor=self.request.user)

    @professor_endpoint(
        summary="Atualizar atividade",
        description="Permite ao professor editar uma atividade criada por ele.",
        request=AtividadeSerializer,
        response=AtividadeSerializer,
        tags=["Atividades"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @professor_endpoint(
        summary="Deletar atividade",
        description="Permite ao professor deletar uma atividade criada por ele.",
        tags=["Atividades"],
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            success_response({}, "Atividade deletada com sucesso"),
            status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        turma = serializer.validated_data.get("turma", None)

        if turma:
            if not turma.professores.filter(id=self.request.user.id).exists():
                raise PermissionDenied("Você não pertence a essa turma")

        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(
            success_response(serializer.data, "Atividade atualizada com sucesso"),
            status=status.HTTP_200_OK
        )


class MinhasAtividadesView(APIView):
    permission_classes = [IsAuthenticated]

    @publico_endpoint(
        summary="Listar atividades",
        description="""
        Retorna atividades conforme o tipo de usuário:

        - PROFESSOR: atividades criadas por ele
        - ALUNO: atividades da turma vinculada
        """,
        response=AtividadeSerializer,
        tags=["Atividades"],
    )
    def get(self, request):
        user = request.user

        # professor vê atividades criadas por ele
        if user.role == "PROFESSOR":
            atividades = Atividade.objects.filter(professor=user)

        # aluno vê atividades da turma
        elif user.role == "ALUNO":
            if not user.turma:
                return Response(
                    {"success": False, "message": "Aluno sem turma"},
                    status=400
                )

            atividades = Atividade.objects.filter(turma=user.turma)

        else:
            return Response(
                {"success": False, "message": "Role inválida"},
                status=403
            )

        atividades = atividades.select_related("turma", "professor")

        paginator = CustomPagination()
        page = paginator.paginate_queryset(atividades, request)

        serializer = AtividadeSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)