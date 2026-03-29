from rest_framework import serializers
from django.utils import timezone

from .models import Resposta


class RespostaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source="aluno.username", read_only=True)
    atividade_titulo = serializers.CharField(source="atividade.titulo", read_only=True)

    class Meta:
        model = Resposta
        fields = [
            "id",
            "conteudo",
            "nota",
            "feedback",
            "atividade",
            "atividade_titulo",
            "aluno_nome",
        ]
        read_only_fields = ["aluno"]

    def validate(self, data):
        request = self.context.get("request")

        if not request:
            return data

        user = request.user

        if self.instance is None:
            atividade = data.get("atividade")

            if user.role != "ALUNO":
                raise serializers.ValidationError("Apenas alunos podem enviar respostas")

            if not user.turma:
                raise serializers.ValidationError("Aluno não está vinculado a uma turma")

            if atividade.turma != user.turma:
                raise serializers.ValidationError("Você não pode responder atividade de outra turma")

            if atividade.data_entrega < timezone.now():
                raise serializers.ValidationError("Prazo da atividade encerrado")

            if Resposta.objects.filter(atividade=atividade, aluno=user).exists():
                raise serializers.ValidationError("Você já enviou resposta para essa atividade")

            return data

        instance = self.instance
        atividade = instance.atividade

        if user.role == "ALUNO":

            if instance.aluno != user:
                raise serializers.ValidationError("Você não pode editar essa resposta")

            if atividade.data_entrega < timezone.now():
                raise serializers.ValidationError("Prazo encerrado")

            if "nota" in data or "feedback" in data:
                raise serializers.ValidationError("Aluno não pode corrigir atividade")

            if "atividade" in data:
                raise serializers.ValidationError("Não é permitido alterar a atividade")

        elif user.role == "PROFESSOR":

            if atividade.professor != user:
                raise serializers.ValidationError("Você não pode corrigir essa atividade")

            if "conteudo" in data:
                raise serializers.ValidationError("Professor não pode alterar resposta do aluno")

            if "nota" not in data:
                raise serializers.ValidationError("Nota é obrigatória")

            nota = data.get("nota")

            if nota is None:
                raise serializers.ValidationError("Nota é obrigatória")

            if not (0 <= nota <= 10):
                raise serializers.ValidationError("Nota deve estar entre 0 e 10")

        else:
            raise serializers.ValidationError("Role inválida")

        return data