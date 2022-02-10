from django.contrib import admin
from channel.models import Channel, Post, ImagePost, Comment

admin.site.register(ImagePost)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("title", "description")
    list_display_links = ("title",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("text",)
    list_display_links = ("text",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("text", "author")
    list_display_links = ("text",)
