from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models
import pypandoc


class Tag(models.Model):
    tag = models.CharField(max_length=50, primary_key=True)

    def __unicode__(self):
        return self.tag

    def get_ordered_posts(self):
        return self.blogpostmodel_set.order_by("-posted_at")


class BlogPostModel(models.Model):
    posted_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    slug = models.SlugField(primary_key=True)
    md_content = models.TextField()
    html_content = models.TextField(default="", editable=False)
    title = models.CharField(max_length=240)

    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        markdown = self.md_content
        self.html_content = pypandoc.convert(markdown, "html", "md")
        super(BlogPostModel, self).save(args, kwargs)

    def __unicode__(self):
        return self.slug

    def is_edited(self):
        timediff = self.edited_at - self.posted_at
        return timediff > timedelta(seconds=1)


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0
            and obj.id != model.objects.get().id):
        raise ValidationError(
            "Can only create one {0} instance".format(model.__name__))


class Author(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    summary_markdown = models.TextField(max_length=1000)
    summary_html = models.TextField(default="", editable=False)
    picture = models.CharField(max_length=200)

    def clean(self):
        validate_only_one_instance(self)

    def save(self, *args, **kwargs):
        markdown = self.summary_markdown
        self.summary_html = pypandoc.convert(markdown, "html", "md")
        super(Author, self).save(args, kwargs)

