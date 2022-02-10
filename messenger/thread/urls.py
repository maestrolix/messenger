from django.urls import path
from thread import views

app_name = 'thread'
urlpatterns = [
    # Threads
    path('thread', views.ThreadList.as_view(), name='thread_list'),
    path('thread/<int:thread_pk>/', views.ThreadDetail.as_view(), name='thread_detail'),
    path('thread-push-notification/<int:thread_pk>/', views.EditPushThread.as_view(), name='push_notif'),
    path('thread-archive/<int:thread_pk>/', views.EditArchiveThread.as_view(), name='thread_archive'),
    path('thread-deleted/<int:thread_pk>/', views.EditDeletedThread.as_view(), name='thread_delete'),
    path('message-list/', views.MessageList.as_view(), name='message_list'),
    path('message-detail/<int:message_pk>/', views.MessageDetail.as_view(), name='message_detail'),
    path('photo-of-message/', views.MessagePhotoList.as_view(), name='photo_list')
]
