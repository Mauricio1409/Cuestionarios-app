from functools import wraps

from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("Acceso denegado: sección solo para staff.")


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("catalog:subjects")
        return view_func(request, *args, **kwargs)

    return _wrapped


class StaffAPIRequiredPermission(BasePermission):
    message = "Acceso denegado: endpoint solo para administradores."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
