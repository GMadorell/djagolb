from django.contrib import admin

from .models import BlogPostModel, Author, Tag


class TagInLine(admin.TabularInline):
    model = BlogPostModel.tags.through


@admin.register(BlogPostModel)
class BlogPostAdmin(admin.ModelAdmin):
    inlines = [
        TagInLine
    ]
    exclude = ("tags", )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [
        TagInLine
    ]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


