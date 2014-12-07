from django.db import models
import pypandoc


class BlogPostModel(models.Model):
    posted_at = models.DateField(auto_now_add=True, auto_now=False)
    edited_at = models.DateField(auto_now=True)

    slug = models.SlugField(primary_key=True)
    md_content = models.TextField()
    html_content = models.TextField(default="", editable=False)
    title = models.CharField(max_length=240)

    def save(self, *args, **kwargs):
        markdown = self.html_content
        html = pypandoc.convert(markdown, "html", "md")
        
        self.html_content = html
        super(BlogPostModel, self).save(args, kwargs)

    def __unicode__(self):
        return self.slug
