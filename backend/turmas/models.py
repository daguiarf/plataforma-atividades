from django.db import models
from django.conf import settings


class Turma(models.Model):
    nome = models.CharField(max_length=100)

    professores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="turmas_professor",
        limit_choices_to={"role": "PROFESSOR"},
        blank=True
    )

    def __str__(self):
        return self.nome    