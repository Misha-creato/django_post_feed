from django.contrib.auth import (
    logout,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
)

from django.views import View
from django.shortcuts import (
    render,
    redirect,
)

from users.models import CustomUser
from users.forms import (
    CustomUserCreationForm,
    LoginForm,
    PasswordResetRequestForm,
)
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
        data = request.POST
        status = register_user(
            request=request,
            data=data,
            form=CustomUserCreationForm,
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
        data = request.POST
        status = login_user(
            request=request,
            data=data,
            form=LoginForm,
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
        user = request.user
        data = request.POST
        status = settings_user(
            request=request,
            data=data,
            user=user,
            form=PasswordChangeForm,
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
        data = request.POST
        status, form_sent = password_reset_request(
            request=request,
            data=data,
            form=PasswordResetRequestForm,
        )
        context = {
            'form_sent': form_sent,
        }
        return render(
            status=status,
            request=request,
            template_name='password_reset.html',
            context=context,
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
        data = request.POST
        status = password_reset_post(
            request=request,
            data=data,
            user=user,
            form=SetPasswordForm,
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
