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
from django.db.models import Q
from django.utils import timezone
import datetime

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
        if content:  # Ensure the content is not empty
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
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
    
    # Get the list of users the logged-in user is following
    following = logged_in_user.profile.following.all()

    # Get suggestions (users not followed by the logged-in user)
    suggestions = User.objects.exclude(id__in=following).exclude(id=logged_in_user.id)[:9]
    
    # Get profiles of the suggested users
    suggested_profiles = Profile.objects.filter(user__in=suggestions)

    # Prepare the suggestions with the first two followers
    suggestion_data = []
    for profile in suggested_profiles:
        followers = profile.followers.all()[:2]  # Get the first two followers
        suggestion_data.append({
            'profile': profile,
            'followers': followers
        })

    # Pass both posts and stories to the context
    context = {
        'posts': posts,
        'stories': stories,
        'logged_in_user': logged_in_user,
        'suggestions': suggestion_data,
    }
    return render(request, 'indexx.html', context)

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



@login_required
def send_message(request, username):
    receiver = get_object_or_404(User, username=username)

    # Update the last seen time in the session
    request.session['last_seen'] = timezone.now().isoformat()  # Store as ISO format string
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('message_thread', username=username)
    else:
        form = MessageForm()

    # Retrieve messages between the sender and receiver
    messages = Message.objects.filter(
        sender=request.user, receiver=receiver
    ) | Message.objects.filter(
        sender=receiver, receiver=request.user
    )
    messages = messages.order_by('timestamp')

    # Last seen
    last_seen_str = request.session.get('last_seen')  # Retrieve the string
    last_seen = datetime.datetime.fromisoformat(last_seen_str) if last_seen_str else None  # Convert back to datetime
    
    return render(request, 'message_thread.html', {
        'receiver': receiver,
        'messages': messages,
        'last_seen': last_seen,  # Pass the datetime object
        'form': form,  # Pass the form to the template
    })


@login_required
def message_list(request):
    sent_messages = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_messages = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    
    # Combine both sender and receiver lists and eliminate duplicates
    user_ids = set(list(sent_messages) + list(received_messages))
    users = User.objects.filter(id__in=user_ids)
    
    return render(request, 'message_list.html', {
        'users': users
    })


@login_required
def create_chat(request, username):
    receiver = get_object_or_404(User, username=username)

    # Check if a message already exists between the logged-in user and the receiver
    existing_message = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) | 
        (Q(sender=receiver) & Q(receiver=request.user))
    ).first()

    
    return redirect('message_thread', username=username)


def following_list(request, username):
    # Get the profile of the user whose following list we want to see
    profile = get_object_or_404(Profile, user__username=username)
    
    # Get the list of users this profile is following
    following = profile.following.all()

    context = {
        'profile': profile,
        'following': following,
    }

    return render(request, 'following_list.html', context)


def followers_list(request, username):
    # Get the user whose followers are being listed
    user = get_object_or_404(User, username=username)
    
    # Get the list of followers from the user's profile
    followers = user.profile.followers.all()
    
    # Pass the followers to the template
    return render(request, 'followers_list.html', {
        'profile_user': user,
        'followers': followers,
    })


@login_required
def upload_reel(request):
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            reel = form.save(commit=False)
            reel.user = request.user
            reel.save()
            return redirect('reel_list')  # Redirect to the reel list page
    else:
        form = ReelForm()
    return render(request, 'upload_reel.html', {'form': form})

@login_required
def reel_list(request):
    reels = Reel.objects.all().order_by('-created_at')
    return render(request, 'reel_list.html', {'reels': reels})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Temporarily disable CSRF protection for the view increment
def view_reel(request, reel_id):
    reel = get_object_or_404(Reel, id=reel_id)

    # Only increment views if the request is a POST
    if request.method == 'POST':
        reel.views += 1
        reel.save()
        return JsonResponse({'status': 'success'})

    context = {
        'reel': reel,
    }
    return render(request, 'view_reel.html', context)