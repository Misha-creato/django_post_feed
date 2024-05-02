from django.urls import path

from posts.views import (
    CreatePostView,
    DetailPostView,
    UpdatePostView,
    DeletePostView,
)

urlpatterns = [
    path(
        'create/',
        CreatePostView.as_view(),
        name='create_post',
    ),
    path(
        '<str:slug>/',
        DetailPostView.as_view(),
        name='detail_post',
    ),
    path(
        'update/<str:slug>/',
        UpdatePostView.as_view(),
        name='update_post',
    ),
    path(
        'delete/<str:slug>/',
        DeletePostView.as_view(),
        name='delete_post',
    )
]
