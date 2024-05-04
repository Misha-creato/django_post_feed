from django.contrib.auth import (
    logout,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.shortcuts import (
    render,
    redirect,
)

from users.services import (
    register_user,
    login_user,
    confirm_email,
    settings_user,
    password_reset_request,
    password_reset_get,
    password_reset_post,
    get_user,
    profile_post,
    send_mail_to_user,
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
        confirm_email(
            request=request,
            url_hash=url_hash,
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
        status = password_reset_get(
            request=request,
            url_hash=url_hash,
        )
        if status == 200:
            return render(
                request=request,
                template_name='password_reset_form.html',
            )
        return redirect('login')

    def post(self, request, url_hash, **kwargs):
        status = password_reset_post(
            request=request,
            url_hash=url_hash,
        )
        if status == 200:
            return redirect('login')
        return render(
            status=status,
            request=request,
            template_name='password_reset_form.html',
        )


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        status, profile = get_user(
            request=request,
            username=username,
        )
        if status != 200:
            return redirect('index')
        context = {
            'profile': profile,
        }
        return render(
            request=request,
            template_name='profile.html',
            context=context,
        )

    def post(self, request, username):
        status = profile_post(
            request=request,
            username=username,
        )
        if status == 404:
            return redirect('index')
        return redirect('profile', username)


class SendMailRequestView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.email_confirmed:
            return redirect('index')
        return render(
            request=request,
            template_name='send_mail_form.html',
        )

    def post(self, request, *args, **kwargs):
        send_mail_to_user(
            request=request,
            user=request.user,
            action='confirm_email',
        )
        return redirect('index')
