from django.shortcuts import render, redirect,get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set hashed password
            user.save()

            # Create a Profile object for the user
            Profile.objects.create(user=user)
            messages.success(request, 'Account created! Please complete your profile.')
            return redirect('create_profile', user_id=user.id)  # Redirect to profile creation page
        
            #login(request, user)  # Automatically log the user in after registration
            #return redirect('index')  # Redirect to the home page
    else:
        form = CustomRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

# Profile Creation View
def create_profile(request, user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            login(request, user)  # Automatically log the user in after registration
            return redirect('test')  # Redirect to the home page
            #return redirect('profile', username=user.username)  # Redirect using 'username'
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'create_profile.html', {'form': form, 'user': user})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('test')  # Redirect to the home page
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to login page

# View for displaying all posts and stories on the index page
def index(request):
    # Get all posts, ordered by latest
    posts = Post.objects.all().order_by('-created_at')
    
    # Get stories created within the last 24 hours
    stories = Story.objects.filter(created_at__gte=timezone.now() - timedelta(hours=24))

    # Pass both posts and stories to the context
    context = {
        'posts': posts,
        'stories': stories,
    }
    return render(request, 'index.html', context)


@login_required
def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            story = form.save(commit=False)  # Create story instance but don't save to DB yet
            story.user = request.user  # Associate the story with the logged-in user
            story.created_at = timezone.now()  # Set the created timestamp
            story.save()  # Save the story to the database
            return redirect('test')  # Redirect to the index or another relevant page
    else:
        form = StoryForm()  # Initialize an empty form

    return render(request, 'add_story.html', {'form': form})


@login_required
def view_story(request, story_id):
    # Fetch the specific story by its ID
    story = get_object_or_404(Story, id=story_id)
    
    # Get the next and previous stories for navigation
    next_story = Story.objects.filter(id__gt=story.id).order_by('id').first()
    prev_story = Story.objects.filter(id__lt=story.id).order_by('-id').first()

    context = {
        'story': story,
        'next_story': next_story,
        'prev_story': prev_story
    }
    return render(request, 'view_story.html', context)

@login_required
def upload_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('test')
    else:
        form = PostForm()
    return render(request, 'upload_post.html', {'form': form})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)  # Get the post or return 404 if not found
    comments = post.comments.all()  # Assuming Post has a related `comments` field
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)




@login_required
def send_message(request, username):
    receiver = get_object_or_404(User, username=username)
    if request.method == 'POST':
        content = request.POST.get('content')
        message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('message_thread', username=username)

    return render(request, 'send_message.html', {'receiver': receiver})

@login_required
def message_thread(request, username):
    receiver = get_object_or_404(User, username=username)
    messages = Message.objects.filter(sender=request.user, receiver=receiver) | \
               Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('timestamp')

    return render(request, 'message_thread.html', {'receiver': receiver, 'messages': messages})

@login_required
def stories(request):
    # Filter only active stories
    stories = Story.objects.filter(created_at__gte=timezone.now() - timedelta(hours=24))
    return render(request, 'stories.html', {'stories': stories})



@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all()  # Assuming each post has a foreign key to the user
    post_count = posts.count()  # Count the number of posts
    context = {
        'user': user,
        'posts': posts,
        'post_count': post_count,  # Add post count to the context
    }
    return render(request, 'profile.html', context)


@login_required
def update_profile_view(request):
    # Get the profile instance for the logged-in user
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})



def toggle_like(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'like_count': post.likes.count()
        })
    
@login_required
def test(request):
     # Get all posts, ordered by latest
    posts = Post.objects.all().order_by('-created_at')
    
    # Get stories created within the last 24 hours
    stories = Story.objects.filter(created_at__gte=timezone.now() - timedelta(hours=24))

     # Get the logged-in user's information
    logged_in_user = request.user

    # Simulate "Suggestions for You" (e.g., users not followed by the logged-in user)
    suggestions = User.objects.exclude(id=logged_in_user.id)[:9]  # Exclude the logged-in user and limit to 5 suggestions
    
    # Get profiles of the suggested users
    suggested_profiles = Profile.objects.filter(user__in=suggestions)

    # Pass both posts and stories to the context
    context = {
        'posts': posts,
        'stories': stories,
        'logged_in_user': logged_in_user,
        'suggestions': suggested_profiles,
    }
    return render(request , 'indexx.html' , context)

# Example view to follow a user
# View to follow a user
@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        request.user.profile.following.add(user_to_follow)
        user_to_follow.profile.followers.add(request.user)  # Add the follower
    return redirect('profile', username=username)

# View to unfollow a user
@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    if user_to_unfollow != request.user:
        request.user.profile.following.remove(user_to_unfollow)
        user_to_unfollow.profile.followers.remove(request.user)  # Remove the follower
    return redirect('profile', username=username)