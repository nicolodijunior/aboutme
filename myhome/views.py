from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Category, User, Comment
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import FileResponse

# Create your views here.


def index(request):
    try:
        posts_qty = Post.objects.all().count()
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post not found"}, status=404)
    
    try:
        last_posts = Post.objects.order_by("-id")[:3]
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post not found"}, status=404)

    return render(request, "myhome/index.html", {
        "posts_qty":posts_qty,
        "last_posts":last_posts,
    })

def post(request):
    post_id = 1
    posts = Post.objects.filter(id=post_id)
    categories = Category.objects.all()
    return render(request, "myhome/blog.html", {
            "posts":posts,
            "categories":categories,
        })

def blog(request, category):
    
    # Loading all posts to paginator
    try:
        p = Paginator(Post.objects.all().order_by("-date_time"), 1)
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post not found"}, status=404)
    page = request.GET.get('page')
    posts = p.get_page(page)
    try:
        categories = Category.objects.all()
    except Category.DoesNotExist:
        return JsonResponse({"error":"Category not found"}, status=404)
    
    if category=="all":
        return render(request, "myhome/blog.html", {
            "posts":posts,
            "categories":categories,
        })
    
def blog_cat(request, id):
    category = Category.objects.get(id=id)   
    posts = category.category_posts.all()
    categories = Category.objects.all()
    return render(request, "myhome/blog.html", {
            "posts":posts,
            "categories":categories,
        })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "myhome/register.html", {
                "message":"Passwords do not match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken or error creating profile."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "myhome/register.html")
 
@login_required
def like_post(request, post_id):
    liked = False
    try:
        p = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post not found"}, status=404)
    
    user = request.user
    if p in user.user_liked_posts.all():
        user.user_liked_posts.remove(p)
    else:
        user.user_liked_posts.add(p)
        liked=True

    likes_qty = p.likes.count()

    return JsonResponse({
        "liked": liked,
        "likes_qty": likes_qty,
        "post_id": post_id,
    })

@login_required
def update_post(request, post_id):
    post = Post.objects.get(id=post_id)  
    user = request.user
    liked = True
    if post not in user.user_liked_posts.all():
        liked = False

    likes_qty = post.likes.count()

    return JsonResponse({
        "liked":liked,
        "likes_qty":likes_qty,
    })



def logout_v(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def login_v(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "myhome/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "myhome/login.html")

@login_required
def comment(request, post_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error":"Category not found"}, status=404)

        new_comment = Comment(user=request.user, text=comment, post=post)
        new_comment.save()
        return redirect(request.META['HTTP_REFERER'])

def loadcv(request):
    return render(request, "myhome/cv.html")
 