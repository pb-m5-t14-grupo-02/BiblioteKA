from rest_framework import permissions
from django.shortcuts import get_object_or_404
from users.models import User


class IsMyOwnAccountSuspended(permissions.BasePermission):
    message = "Your account is suspended, regularize your situation so you can rent more books"

    def has_permission(self, request, view):
        return not request.user.is_suspended


class IsStudentSuspended(permissions.BasePermission):
    message = "This student is suspended, then he can't loan any books"

    def has_permission(self, request, view):
        user = get_object_or_404(User, id=request.parser_context["kwargs"]["student_id"])
        return not user.is_suspended
