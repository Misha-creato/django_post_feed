from django.urls import path

from posts.views import (
    CreatePostView,
    DetailPostView,
    UpdatePostView,
    DeletePostView,
    SearchView, HidePostView,
)


urlpatterns = [
    path(
        'create/',
        CreatePostView.as_view(),
        name='create_post',
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
    ),
    path(
        'search/',
        SearchView.as_view(),
        name='search',
    ),
    path(
        'hide/<str:slug>/',
        HidePostView.as_view(),
        name='hide_post',
    ),
    path(
        '<str:slug>/',
        DetailPostView.as_view(),
        name='detail_post',
    ),
]
