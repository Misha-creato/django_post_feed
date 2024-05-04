from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.shortcuts import (
    render,
    redirect,
)

from posts.services import (
    update_or_create_post,
    get_post,
    delete_post, search_posts, hide_post,
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
        status, post = get_post(
            request=request,
            slug=slug,
            detail=True,
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
        status, post = get_post(
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
        status, post = get_post(
            request=request,
            slug=slug,
        )
        if status == 200:
            status, post = update_or_create_post(
                request=request,
                action='обновлен',
                slug=slug,
            )
            if status == 200:
                return redirect('detail_post', post.slug)
            return redirect('update_post', slug)
        return redirect('index')


class DeletePostView(LoginRequiredMixin, View):
    def post(self, request, slug):
        status, post = get_post(
            request=request,
            slug=slug,
        )
        if status == 200:
            delete_post(
                request=request,
                post=post,
            )
        return redirect('index')


class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        status, posts = search_posts(
            request=request,
        )
        context = {
            'posts': posts,
        }
        return render(
            status=status,
            request=request,
            template_name='search_results.html',
            context=context,
        )


class HidePostView(LoginRequiredMixin, View):
    def post(self, request, slug):
        hide_post(
            request=request,
            slug=slug,
        )
        return redirect(request.META.get('HTTP_REFERER', 'index'))
