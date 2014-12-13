from django.contrib import admin

# Register your models here.
from .models import BlogPostModel, Author, Tag


@admin.register(BlogPostModel)
class BlogPostAdmin(admin.ModelAdmin):
    exclude = ("html_content", )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


class TagInLine(admin.TabularInline):
    pass
    # model = Tag
    # fields = ["tag"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
    # inlines = [
    #     TagInLine
    # ]
    # exclude = (Tag, )


