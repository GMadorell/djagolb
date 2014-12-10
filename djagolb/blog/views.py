from django.contrib.sites.models import Site
from django.views import generic

from .models import BlogPostModel


class BlogIndexView(generic.ListView):
    template_name = "blog/blog_index.html"
    model = BlogPostModel

    def get_queryset(self):
        return self.model.objects.order_by("-posted_at")


class BlogPostDetail(generic.DetailView):
    template_name = "blog/blogpost.html"
    context_object_name = "blogpost"
    model = BlogPostModel

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetail, self).get_context_data(**kwargs)
        context["site"] = Site.objects.get_current()
        return context

    

