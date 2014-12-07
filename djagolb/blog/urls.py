from django.conf.urls import patterns, url
from .views import BlogIndexView, BlogPostDetail

urlpatterns = patterns('',
    url(r"^$", BlogIndexView.as_view(), name="blog_index"),
    url(r"^post/(?P<slug>.*?)/$", BlogPostDetail.as_view(), name="blogpost"),
)
