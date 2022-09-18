from django.contrib import admin

from .models import Post,Caption, Comment

admin.site.register(Post)

class CaptionAdmin(admin.ModelAdmin):
    list_display = ("tag", "id",)
admin.site.register(Caption, CaptionAdmin)
admin.site.register(Comment)
