from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/api/', include("account.urls")),
    path('channel/api/', include("channel.urls")),
    path('thread/api/', include("thread.urls")),
]
