from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import (
    render,
    redirect,
)
from django.views import View

from posts.models import Post
from posts.services import (
    create_post,
    update_post_request,
)

User = get_user_model()


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='create_post.html',
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.POST
        files = request.FILES
        status, post = create_post(
            request=request,
            user=user,
            data=data,
            files=files,
        )
        if status == 200:
            return redirect('detail_post', post.pk)
        return render(
            request=request,
            template_name='create_post.html',
        )


class DetailPostView(View):
    def get(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        context = {
            'post': post,
        }
        return render(
            request=request,
            template_name='detail_post.html',
            context=context,
        )


class UpdatePostView(View): # доделать
    def get(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        context = {
            'post': post,
        }
        return render(
            request=request,
            template_name='update_post.html',
            context=context,
        )

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        data = request.POST
        files = request.FILES
        status, post = update_post_request(
            request=request,
            post=post,
            data=data,
            files=files,
        )
        if status == 200:
            return redirect('detail_post', post.pk)
        return render(
            request=request,
            template_name='update_post.html',
        )