from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        PROFESSOR = "PROFESSOR", "Professor"
        ALUNO = "ALUNO", "Aluno"

    role = models.CharField(max_length=20, choices=Role.choices)

    # aqui garantimos que aluno precisa estar em uma turma
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alunos"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"