from django.contrib import admin

from .models import Post

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created']
    list_filter = ['date_created']
