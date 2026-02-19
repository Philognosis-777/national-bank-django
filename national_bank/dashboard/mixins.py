from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Allow access only to users with role == 'admin' or superusers."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        role = getattr(user, 'role', None)
        return user.is_superuser or (role == 'admin')

    def handle_no_permission(self):
        raise PermissionDenied
