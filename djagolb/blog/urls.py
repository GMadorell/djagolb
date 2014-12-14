from django.conf.urls import patterns, url
from .views import BlogIndexView, BlogPostDetail, ArchiveView, AboutView, \
    TagView

urlpatterns = patterns('',
    url(r"^$", BlogIndexView.as_view(), {"page": 1}, name="blog_index"),
    url(r"^page/(?P<page>\d+)/$", BlogIndexView.as_view(), name="blog_index_page"),
    url(r"^post/(?P<slug>.*?)/$", BlogPostDetail.as_view(), name="blogpost"),
    url(r"^archive/$", ArchiveView.as_view(), name="archive"),
    url(r"about/$", AboutView.as_view(), name="about"),
    url(r"tags/$", TagView.as_view(), name="tags")
)
