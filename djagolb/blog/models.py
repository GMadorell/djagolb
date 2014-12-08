from django.db import models
import pypandoc


class BlogPostModel(models.Model):
    posted_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    edited_at = models.DateTimeField(auto_now=True)

    slug = models.SlugField(primary_key=True)
    md_content = models.TextField()
    html_content = models.TextField(default="", editable=False)
    title = models.CharField(max_length=240)

    def save(self, *args, **kwargs):
        markdown = self.md_content
        self.html_content = pypandoc.convert(markdown, "html", "md")
        super(BlogPostModel, self).save(args, kwargs)

    def __unicode__(self):
        return self.slug
