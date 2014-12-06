from django.shortcuts import render

# Create your views here.
from django.views import generic

from .models import BlogPostModel



class BlogIndexView(generic.ListView):
    template_name = "blog/blog_index.html"
    model = BlogPostModel
    

