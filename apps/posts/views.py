from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import (
    render,
    redirect,
)
from django.views import View

from posts.services import (
    update_or_create_post,
    find_post,
    delete_post,
)

User = get_user_model()


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='create_post.html',
        )

    def post(self, request, *args, **kwargs):
        status, post = update_or_create_post(
            request=request,
            action='создан',
        )
        if status == 200:
            return redirect('detail_post', post.slug)
        return render(
            request=request,
            template_name='create_post.html',
        )


class DetailPostView(LoginRequiredMixin, View):
    def get(self, request, slug):
        status, post = find_post(
            request=request,
            slug=slug,
        )
        if status == 200:
            context = {
                'post': post,
            }
            return render(
                request=request,
                template_name='detail_post.html',
                context=context,
            )
        return redirect('index')


class UpdatePostView(LoginRequiredMixin, View):
    def get(self, request, slug):
        status, post = find_post(
            request=request,
            slug=slug,
        )
        if status == 200:
            context = {
                'post': post,
            }
            return render(
                request=request,
                template_name='update_post.html',
                context=context,
            )
        return redirect('index')

    def post(self, request, slug):
        status, post = update_or_create_post(
            request=request,
            action='обновлен',
        )
        if status == 200:
            return redirect('detail_post', post.slug)
        return render(
            request=request,
            template_name='update_post.html',
        )


class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, slug):
        status, post = find_post(
            request=request,
            slug=slug,
        )
        if status == 200:
            delete_post(
                request=request,
                post=post,
            )
        return redirect('index')
