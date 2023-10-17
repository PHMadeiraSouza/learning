import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

from .models import User, Post, Follow

def get_mytimezone_date(original_datetime):
        new_datetime = datetime.strptime(original_datetime, '%Y-%m-%d')
        tz = timezone.get_current_timezone()
        timzone_datetime = timezone.make_aware(new_datetime, tz, True)
        return timzone_datetime.date()

def index(request):
    page_number = request.GET.get('page')
    allposts = Post.objects.all().order_by('-timestamp')
    posts = Paginator(allposts, 10).get_page(page_number)
    return render(request, "network/index.html", {
        "posts": posts,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            create_follow = Follow.objects.create(user_followed=user)
            create_follow.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def createpost(request):
    if request.method == "POST":
        body = json.loads(request.body)
        content = body.get("content", "")
        timestamp = timezone.now()

        try:
            new_post = Post.objects.create(content=content, poster= request.user, timestamp=timestamp)
            new_post.save()
        except:
            return HttpResponse(status=500)
        return HttpResponse(status=201)
    pass

@csrf_exempt
@login_required
def editpost(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.poster:
        if request.method == "POST":
            body = json.loads(request.body)
            content = body.get("content", "")
            try:
                post.content = content
                post.save()
            except:
                return HttpResponse(status=500)

            try:
                post.edited = True
                post.save()
            except:
                return HttpResponse(status=500)
            return HttpResponse(status=204)
        return HttpResponse(status=405)

def user(request, user_id):
    user = User.objects.get(id=user_id)
    requestuser = request.user

    try:
        following = Follow.objects.filter(followers=user)
    except:
        following = []

    try:
        follow = Follow.objects.get(user_followed=user)
        followers = follow.followers.all()
    except:
        followers = []


    if request.user.is_authenticated:
        isfollowing = requestuser in followers
    else:
        isfollowing = False

    requestuserisuser = requestuser.id == user.id
    page_number = request.GET.get('page')
    allposts = Post.objects.filter(poster_id=user_id).order_by("timestamp").all()
    posts = Paginator(allposts, 10).get_page(page_number)
    return render(request, "network/userpage.html", {
        "user_page": user,
        "following": following,
        "followers": followers,
        "isfollowing": isfollowing,
        "requestuserisuser": requestuserisuser,
        "posts": posts,
        "user_id": user_id,
    })

@login_required
@csrf_exempt
def followuser(request, user_id):
    if request.method == 'POST':
        request_user = request.user
        user_followed = User.objects.get(id=user_id)
        if request.user is not user_followed:
            follow = Follow.objects.get(user_followed=user_followed)
            follow.followers.add(request_user)
            return HttpResponse(status=204)
    return HttpResponse(status=405)

@login_required
@csrf_exempt
def unfollowuser(request, user_id):
    if request.method == 'POST':
        request_user = request.user
        user_followed = User.objects.get(id=user_id)
        if request.user is not user_followed:
            follow = Follow.objects.get(user_followed=user_followed)
            follow.followers.remove(request_user)
            return HttpResponse(status=204)
    return HttpResponse(status=405)

def following(request):
    following = Follow.objects.values_list('user_followed',flat= True).filter(followers= request.user.id)
    if following:
        page_number = request.GET.get('page')
        allposts = Post.objects.filter(poster_id__in=(following)).order_by('-timestamp')
        posts = Paginator(allposts, 10).get_page(page_number)
        if posts:
            message = "something went wrong"
        else:
            posts = False
            message = "the users you follow don't have any posts"
    else:
        posts = False
        message = "you currently don't follow any user"

    return render(request, "network/following.html", {
    "posts": posts,
    "message":message,
    })

@csrf_exempt
@login_required
def likepost(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user is not post.poster:
        if request.method == "POST":
            request_user = request.user
            post.likes.add(request_user)
            return HttpResponse(status=204)
        return HttpResponse(status=405)
    return HttpResponse(status=403)

@csrf_exempt
@login_required
def unlikepost(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user is not post.poster:
        if request.method == "POST":
            request_user = request.user
            post.likes.remove(request_user)
            return HttpResponse(status=204)
        return HttpResponse(status=405)
    return HttpResponse(status=403)