from django.contrib import admin
from thread.models import Thread, Message, MessagePhoto

admin.site.register(MessagePhoto)
admin.site.register(Thread)
admin.site.register(Message)
