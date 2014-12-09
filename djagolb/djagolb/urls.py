from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r"^", include("blog.urls", namespace="blog")),
    url(r'^blog/comments/', include('fluent_comments.urls')),
)
