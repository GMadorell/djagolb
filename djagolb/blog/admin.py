from django.contrib import admin

# Register your models here.
from .models import BlogPostModel


class BlogPostAdmin(admin.ModelAdmin):
    exclude = ("html_content", )

admin.site.register(BlogPostModel, BlogPostAdmin)
