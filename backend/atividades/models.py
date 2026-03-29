from django.db import models
from django.conf import settings


class Atividade(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_entrega = models.DateTimeField()

    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="atividades"
    )

    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.CASCADE,
        related_name="atividades"
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo