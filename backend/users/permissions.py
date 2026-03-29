from rest_framework.permissions import BasePermission


class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "PROFESSOR"


class IsAluno(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ALUNO"