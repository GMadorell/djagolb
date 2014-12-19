from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r"^", include("blog.urls", namespace="blog")),
    url(r'^articles/comments/', include('django.contrib.comments.urls')),
)
