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
from django import forms

# Create your views here.

class registerForm(forms.Form):
    username = forms.CharField(label="Username", max_length=64)
    email = forms.EmailField(label="Email", max_length=64)
    password = forms.CharField(label="Password", max_length=64, widget=forms.PasswordInput)
    confirmation = forms.CharField(label="Confirmation", max_length=64, widget=forms.PasswordInput)
    #give a class for all inputs of the form to be able to style them
    def __init__(self, *args, **kwargs):
        super(registerForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'log_info'})
        self.fields['email'].widget.attrs.update({'class': 'log_info'})
        self.fields['password'].widget.attrs.update({'class': 'log_info'})
        self.fields['confirmation'].widget.attrs.update({'class': 'log_info'})
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username
    
    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password)<8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password


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

def post(request, post_id):
    posts = Post.objects.filter(id=post_id)
    is_event = posts.first().category.name == "Events"
    categories = Category.objects.all()
    return render(request, "myhome/blog.html", {
            "event":is_event,
            "posts":posts,
            "categories":categories,
        })

def blog(request, category):
    
    # Loading all posts to paginator
    if category=="all":
        try:
            p = Paginator(Post.objects.exclude(category__name="Events").order_by("-date_time"), 1)
        except Post.DoesNotExist:
            return JsonResponse({"error":"Post not found"}, status=404)
        page = request.GET.get('page')
        posts = p.get_page(page)
        try:
            categories = Category.objects.exclude(name="Events").all()
        except Category.DoesNotExist:
            return JsonResponse({"error":"Category not found"}, status=404)
        
        return render(request, "myhome/blog.html", {
            "posts":posts,
            "categories":categories,
        })
    
    if category=="Events":
        try:
            p = Paginator(Post.objects.filter(category__name="Events").order_by("-date_time"), 1)
        except Post.DoesNotExist:
            return JsonResponse({"error":"Post not found"}, status=404)
        page = request.GET.get('page')
        posts = p.get_page(page)
        try:
            categories = Category.objects.all()
        except Category.DoesNotExist:
            return JsonResponse({"error":"Category not found"}, status=404)
        
        return render(request, "myhome/blog.html", {
            "posts":posts,
            "categories":categories,
            "event":True,
        })
        
def blog_cat(request, id):
    category = Category.objects.get(id=id)   
    posts = category.category_posts.exclude(id="4").all()
    categories = Category.objects.exclude(name="Events").all()
    return render(request, "myhome/blog.html", {
            "posts":posts,
            "categories":categories,
        })

def register(request):
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]
            if password != confirmation:
                return render(request, "myhome/register.html", {
                    "message":"Passwords do not match.",
                    "form":form,
                })
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError as e:
                print(e)
                return render(request, "myhome/register.html", {
                    "message": "Error creating account."
                })
            
            login(request, user)
            return HttpResponseRedirect(reverse("index"))       
        else:
            return render(request, "myhome/register.html", {
                "form":form,
            })
    else:
        form = registerForm()
        return render(request, "myhome/register.html", {
            "form":form,
        })
 
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
 