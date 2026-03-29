from rest_framework import serializers
from .models import Atividade


class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = '__all__'
        read_only_fields = ['professor']

    def validate(self, data):
        if not data.get("turma"):
            raise serializers.ValidationError("Turma é obrigatória")
        return data