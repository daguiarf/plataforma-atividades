from django.db import models
from django.conf import settings


class Resposta(models.Model):
    atividade = models.ForeignKey(
        "atividades.Atividade",
        on_delete=models.CASCADE,
        related_name="respostas"
    )

    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="respostas"
    )

    conteudo = models.TextField()

    nota = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("atividade", "aluno")

    def __str__(self):
        return f"{self.aluno} - {self.atividade}"