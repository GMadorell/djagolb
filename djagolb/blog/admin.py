from django.contrib import admin

# Register your models here.
from .models import BlogPostModel, Author


@admin.register(BlogPostModel)
class BlogPostAdmin(admin.ModelAdmin):
    exclude = ("html_content", )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


