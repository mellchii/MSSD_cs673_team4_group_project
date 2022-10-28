import re
from venv import create
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render , redirect
from pscmodels.models import User, Posts, Shared, Comments, Following, Archive, Vote, Profile
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .forms import SetPasswordForm, PasswordResetForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.password_validation import validate_password

@login_required
def changePassword(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'manageaccounts/password_reset_confirm.html', {'form': form})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request,('Passwords must match.'))
            return redirect('register')
        #make sure email is valid
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request,('Email is invalid'))
            return redirect('register')             
        # strong password validation
        try:
            validate_password(password, None, None)
        except ValidationError:
            messages.warning(request,('Please do not create passwords that are: too similar to the user details, below length of 8, too common or all numeric'))
            return redirect('register')
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(user=user)

        except IntegrityError:
            messages.warning(request,('Username already taken.'))
            return redirect('register')
 
        login(request, user)
        messages.success(request,('New User '+ username + ' Created'))
        return redirect("home")
    else:
        user = request.user
        if (user.is_authenticated):
            return redirect("home")
        else:
            return render(request, "manageaccounts/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request,('Login Successful'))
            return redirect('home')
        else:
            messages.warning(request,('Error Logging In, Try Again...'))
            return redirect('login')
    else:
        user = request.user
        if (user.is_authenticated):
            return redirect("home")
        else:
            return render(request, "manageaccounts/login.html")

def logout_view(request):
    logout(request)
    messages.warning(request,('Log Out Successful'))
    return redirect('home')


def profile(request, username):
    post = Posts.objects.filter(creator__username=username).all()
    count = Posts.objects.filter(creator__username=username).count()
    followers = Following.objects.filter(following__username=username).count()
    followings = Following.objects.filter(follower__username=username).count()
    usernameS = get_object_or_404(User, username=username)
    user = request.user
    print (usernameS)

    pager = Paginator(post, 10)  # Show 10 posts per page.
    page_number = request.GET.get('page', 1)
    page = pager.page(page_number)

    upvoteCount = 0
    downvoteCount = 0
    for i in post:
        upvoteCount += i.upvotes
        downvoteCount += i.downvotes

    return render(request, "manageaccounts/profile.html", {
        "posts": page,
        "username": usernameS,
        "user": user,
        "count": count,
        "followers": followers,
        "followings": followings,
        'up': upvoteCount,
        'down': downvoteCount
    })
def bookmark(request, username):
    if request.user.is_authenticated:
        favorites = Posts.objects.filter(favorites=request.user).all()

        return render(request, "manageaccounts/favorites.html", {
            "favorites": favorites,
    })

                        
def userFeed(request,username):
    post = Posts.objects.filter(creator=request.user).all()
    pager = Paginator(post, 10) # Show 10 posts per page.
    page_number = request.GET.get('page', 1)
    page = pager.page(page_number)


    return render(request, "manageaccounts/userFeed.html", {
        "posts": page,
        "user": request.user,
        "username": username,
})

def editProfile(request, username):
    if (username == request.user.username):
        user_obj = request.user
        profile_obj = request.user.profile
        
        u_form = UserUpdateForm(instance=user_obj)
        p_form = ProfileUpdateForm(instance=profile_obj)

        context = {
            'u_form': u_form,
            'p_form' : p_form,
            'user': request.user,
            'username': user_obj
        }

        if (request.method == 'POST'):
            u_form = UserUpdateForm(request.POST, request.FILES, instance=user_obj)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
            if (u_form.is_valid()):
                if (p_form.is_valid()):
                    u_form.save()
                    p_form.save()
                    messages.success(request,('User Profile Updated'))
                    return redirect('profile', username)

        return render(request, "manageaccounts/editProfile.html", context)
    else:
        messages.warning(request,('Permission Denied'))
        return redirect("home")


def deleteUser(request,username):
    if (request.user.username == username):
        try:
            user = User.objects.get(username = username)
            logout(request)
            user.delete()
            messages.success(request, "User "+ username +" is deleted") 
            return redirect('home')  
        except:
            messages.error(request, "User doesnot exist")    
            return redirect('home')

    else:
        messages.warning(request,('Permission Denied'))
        return redirect("home")
