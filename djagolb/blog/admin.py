from django.contrib import admin

# Register your models here.
from .models import BlogPostModel


class BlogPostAdmin(admin.ModelAdmin):
    pass

admin.site.register(BlogPostModel, BlogPostAdmin)
