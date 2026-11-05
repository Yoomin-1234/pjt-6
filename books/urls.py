from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    # 도서 기능
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    # 쓰레드 기능
    path("<int:book_pk>/threads/create/", views.thread_create, name="thread_create"),
    path(
        "<int:book_pk>/threads/<int:thread_pk>/",
        views.thread_detail,
        name="thread_detail",
    ),
    path(
        "<int:book_pk>/threads/<int:thread_pk>/update/",
        views.thread_update,
        name="thread_update",
    ),
    path(
        "<int:book_pk>/threads/<int:thread_pk>/delete/",
        views.thread_delete,
        name="thread_delete",
    ),
    path("<int:book_pk>/threads/<int:thread_pk>/likes/", views.like, name="like"),
    # 댓글 기능 (F627)
    path(
        "<int:book_pk>/threads/<int:thread_pk>/comments/",
        views.comment_create,
        name="comment_create",
    ),
    path(
        "<int:book_pk>/threads/<int:thread_pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
]
