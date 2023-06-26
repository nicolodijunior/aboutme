from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("blog/<str:category>", views.blog, name="blog"),
    path("blog_cat/<int:id>", views.blog_cat, name="blog_cat"),
    path("register", views.register, name="register"),
    path("logout", views.logout_v, name="logout_v"),
    path("login_v", views.login_v, name="login_v"),
    path("blog/all/like_post/<int:post_id>", views.like_post, name="like_post"),
    path("blog/all/update_post/<int:post_id>", views.update_post, name="update_post"),
    path("blog/all/comment/<int:post_id>", views.comment, name="comment"),
    path("post/<int:post_id>", views.post, name="post"),
    path("cv", views.loadcv, name="loadcv"),
]