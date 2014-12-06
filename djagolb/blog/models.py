from django.db import models


class BlogPostModel(models.Model):
    posted_at = models.DateField(auto_now_add=True, auto_now=False)
    edited_at = models.DateField(auto_now=True)

    slug = models.SlugField()
    content = models.TextField()
    title = models.CharField(max_length=240)
