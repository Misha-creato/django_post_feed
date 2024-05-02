from django.contrib.auth import (
    logout,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.shortcuts import (
    render,
    redirect,
)

from users.models import CustomUser

from users.services import (
    register_user,
    login_user,
    confirm_email,
    settings_user,
    password_reset_request,
    password_reset_get,
    password_reset_post,
)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='register.html',
        )

    def post(self, request, *args, **kwargs):
        status = register_user(
            request=request,
        )
        if status == 200:
            return redirect('login')
        return render(
            status=status,
            request=request,
            template_name='register.html',
        )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='login.html',
        )

    def post(self, request, *args, **kwargs):
        status = login_user(
            request=request,
        )
        if status == 200:
            return redirect('index')
        return render(
            status=status,
            request=request,
            template_name='login.html',
        )


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request=request)
        return redirect('index')


class EmailConfirmView(View):
    def get(self, request, url_hash):
        user = CustomUser.objects.filter(url_hash=url_hash).first()
        confirm_email(
            request=request,
            user=user,
        )
        return redirect('index')


class SettingsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='settings.html',
        )

    def post(self, request, *args, **kwargs):
        status = settings_user(
            request=request,
        )
        return render(
            status=status,
            request=request,
            template_name='settings.html',
        )


class PasswordResetRequestView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='password_reset.html',
        )

    def post(self, request, *args, **kwargs):
        status = password_reset_request(
            request=request,
        )
        return render(
            status=status,
            request=request,
            template_name='password_reset.html',
        )


class PasswordResetView(View):
    def get(self, request, url_hash):
        user = CustomUser.objects.filter(url_hash=url_hash).first()
        status = password_reset_get(
            request=request,
            user=user,
        )
        if status == 200:
            return render(
                request=request,
                template_name='password_reset_form.html',
            )
        return redirect('login')

    def post(self, request, url_hash, **kwargs):
        user = CustomUser.objects.filter(url_hash=url_hash).first()
        status = password_reset_post(
            request=request,
            user=user,
        )
        if status == 200:
            return redirect('login')
        return render(
            status=status,
            request=request,
            template_name='password_reset_form.html',
        )


class ProfileView(View):
    def get(self, request, username):
        user_profile = CustomUser.objects.filter(username=username).first()
        context = {
            'user_profile': user_profile,
        }
        return render(
            request=request,
            template_name='profile.html',
            context=context,
        )
