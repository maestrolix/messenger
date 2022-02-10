from django.db import models
from account.models import AdvUser

from config.global_services import get_upload_path


class Channel(models.Model):
    """ Каналы месенжера """
    title = models.CharField(max_length=30, verbose_name='Название канала')
    participants = models.ManyToManyField(AdvUser, related_name='channels', verbose_name='Пользователи канала')
    avatar = models.ImageField(upload_to=get_upload_path('images/channel/avatars/'),
                               default='static/messenger/images/default_image.jpg')
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name='Описание канала')
    admins = models.ManyToManyField(AdvUser, related_name='admin_of_channels', verbose_name='Администраторы канала')
    creator = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='creator_of_channels', null=True)
    black_list = models.ManyToManyField(AdvUser, related_name='in_black_list_channels',
                                        verbose_name='Пользователи в чёрном списке')

    class Meta:
        db_table = 'channel'
        verbose_name_plural = 'Канал'
        verbose_name = 'Каналы'


class Post(models.Model):
    """ Публикации каналов """
    text = models.TextField(max_length=500, verbose_name='Текст поста')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='posts', verbose_name='Канал поста')

    class Meta:
        db_table = 'post'
        verbose_name_plural = 'Пост канала'
        verbose_name = 'Посты каналов'


class ImagePost(models.Model):
    """ Фотографии, которые прикрепляются к постам """
    image = models.ImageField(upload_to=get_upload_path('images/channel/posts/images/'),
                              verbose_name='Фотография поста')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images',
                             verbose_name='Фотографии в посте')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True, related_name='channel_images',
                                verbose_name='Фотографии на канале')
    sender = models.ForeignKey(AdvUser, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='user_post_images', verbose_name='Фотографии пользователя на каналах')
    description = models.TextField(max_length=500, null=True, verbose_name='Описание медиа для поисковиков')

    class Meta:
        db_table = 'image_post'
        verbose_name_plural = 'Фотография поста'
        verbose_name = 'Фотографии постов'


class VideoPost(models.Model):
    """ Видео, которые прикрепляются к постам """
    image = models.ImageField(upload_to=get_upload_path('videos/channel/posts/videos/'), verbose_name='Видио поста')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_videos',
                             verbose_name='Видеозапись поста')
    description = models.TextField(max_length=500, verbose_name='Описание медиа для поисковиков')

    class Meta:
        db_table = 'video_post'
        verbose_name_plural = 'Видио поста'
        verbose_name = 'Видио постов'


class Comment(models.Model):
    """ Комментарии постов """
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='user_comments',
                               verbose_name='Автор комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments',
                             verbose_name='Пост комментария')
    text = models.TextField(max_length=1000, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
        verbose_name_plural = 'Комментарий поста'
        verbose_name = 'Комментарии постов'
