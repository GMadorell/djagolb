from django.conf.urls import patterns, url
from .views import BlogIndexView, BlogPostDetail, ArchiveView

urlpatterns = patterns('',
    url(r"^$", BlogIndexView.as_view(), name="blog_index"),
    url(r"^post/(?P<slug>.*?)/$", BlogPostDetail.as_view(), name="blogpost"),
    url(r"^archive/$", ArchiveView.as_view(), name="archive")
)
