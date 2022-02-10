from django.urls import path
from channel import views

app_name = 'channel'
urlpatterns = [
    # Channels
    path('channels/', views.ChannelList.as_view(), name='channels_list'),
    path('channel/<int:channel_pk>/', views.ChannelDetail.as_view(), name='channel_detail'),
    path('delete-user-from-channel/<int:channel_pk>/<int:user_pk>/', views.DeleteUserFromChannel.as_view(),
         name='delete_user_by_admin'),
    path('channel-subscribe-unsubscribe/<int:channel_pk>/', views.AddOrDeleteFromChannel.as_view(),
         name='subscriptions_user'),
    path('post-detail/<int:post_pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post-list/<int:channel_pk>/', views.CreatePost.as_view(), name='post_list'),
    path('comment/', views.CommentList.as_view(), name='comment_create'),
    path('comment/<int:comment_pk>/', views.CommentDetail.as_view(), name='comment_detail'),
    path('photo-of-post/', views.PostPhotoList.as_view(), name='post_photo_list'),
    path('delete-admin/', views.DeleteAdmin.as_view(), name='delete_admin'),
    path('add-admin/', views.AddAdmin.as_view(), name='add_admin'),
]
