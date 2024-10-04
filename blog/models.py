from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=50 , blank=True)
    about=models.CharField(max_length=150)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png')
    followers = models.ManyToManyField(User, related_name='following_profiles', blank=True)
    following = models.ManyToManyField(User, related_name='followers_profiles', blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(max_length=2200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    
    def __str__(self):
        return self.caption[:20]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Comment on {self.post.caption[:20]}'
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # Fields for media uploads
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'
    

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_active(self):
        return timezone.now() < self.created_at + timedelta(hours=24)

    def __str__(self):
        return f'{self.user.username} Story'
    


class Reel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reels')
    video = models.FileField(upload_to='reels/')  # To store video files
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_reels', blank=True)
    views = models.PositiveIntegerField(default=0)  # Field to track views

    def __str__(self):
        return f'Reel by {self.user.username}'

