from django.shortcuts import render

# Create your views here.
from django.views import generic


class BlogIndexView(generic.TemplateView):
    template_name = "blog/blog_index.html"
    

