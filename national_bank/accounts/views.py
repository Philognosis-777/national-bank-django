from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RedirectAuthenticatedUserMixin:
    """Prevent authenticated users from accessing auth pages."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # role-based redirect
            if hasattr(request.user, 'role') and request.user.role == CustomUser.ROLE_ADMIN:
                return redirect('/home/')
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(RedirectAuthenticatedUserMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


class LoginView(RedirectAuthenticatedUserMixin, auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        remember = form.cleaned_data.get('remember_me')
        # If remember is False, session will expire at browser close
        if not remember:
            self.request.session.set_expiry(0)
        else:
            # Use default session expiry age
            self.request.session.set_expiry(None)
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == CustomUser.ROLE_PUBLIC:
            return '/home/'
        return '/home/'


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('core:intro')
