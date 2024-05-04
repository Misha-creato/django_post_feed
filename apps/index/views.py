from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from index.services import get_posts


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status, posts = get_posts(
            request=request,
        )
        context = {
            'posts': posts,
        }
        return render(
            status=status,
            request=request,
            template_name='index.html',
            context=context,
        )
