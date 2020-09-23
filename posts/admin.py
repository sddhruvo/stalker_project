from django.contrib import admin
from .models import Post, Comment

class CommentAdmin(admin.StackedInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin,]

    class Meta:
       model = Comment