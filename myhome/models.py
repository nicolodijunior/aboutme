
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name="Project category")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name="Post creator")
    title = models.CharField(max_length=64, verbose_name="Post title")
    text = models.CharField(max_length=700, verbose_name="Post description text")
    date_time = models.DateTimeField(auto_now=True, verbose_name="Time and date of creation")
    github_link = models.CharField(max_length=80, verbose_name="Github link")
    img_path = models.CharField(max_length=200, verbose_name="Image path")
    video_path = models.CharField(max_length=200, verbose_name="Video path")
    tags = models.CharField(max_length=50, verbose_name="Post tags")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_posts", verbose_name="Post category")
    likes = models.ManyToManyField(User, blank=True, related_name="user_liked_posts", verbose_name="Comment Likes")
    
    def get_comments(self):
        return self.post_comments.order_by(F('date_time').desc())
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", verbose_name="Author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments", verbose_name="Post of the comment")
    likes = models.ManyToManyField(User, blank=True, related_name="user_liked_comments", verbose_name="Comment Likes")
    date_time = models.DateTimeField(auto_now=True, verbose_name="Time and date of creation")
    text = models.CharField(max_length=700, verbose_name="Post description text")

