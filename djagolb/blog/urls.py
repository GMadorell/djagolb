from django.conf.urls import patterns, url
from .views import BlogIndexView

urlpatterns = patterns('',
    url(r"^$", BlogIndexView.as_view()),
)
