from django.urls import path

from posts.views import (
    CreatePostView,
    DetailPostView,
)

urlpatterns = [
    path(
        'create/',
        CreatePostView.as_view(),
        name='create_post',
    ),
    path(
        '<int:pk>/',
        DetailPostView.as_view(),
        name='detail_post',
    )
]