from django.urls import path
from . import views

urlpatterns = [
    # User Profiles
    path('profile/<str:username>/', views.profile_view, name='profile'),
    
    # Follow/Unfollow
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    
    # Messaging
    path('messages/<str:username>/', views.message_thread, name='message_thread'),
    path('messages/<str:username>/send/', views.send_message, name='send_message'),

    # Stories
    path('stories/', views.stories, name='stories'),
    path('story/<int:story_id>/', views.view_story, name='view_story'),
    path('add_story/', views.add_story, name='add_story'),
    
    # Posts
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/<int:id>/like/', views.toggle_like, name='toggle_like'),
    path('post', views.upload_post , name='upload_post') ,
    
    # Home Page (Feed)
    #path('', views.index, name='index'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_profile/<int:user_id>/', views.create_profile, name='create_profile'),
    path('update_profile/', views.update_profile_view, name='update_profile'),
    path('', views.test , name="test"),
]
