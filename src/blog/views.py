from collections import OrderedDict, Iterable
import pdb
from django.contrib.sites.models import Site
from django.http import Http404
from django.views import generic
from django.views.generic.base import ContextMixin

from .models import BlogPostModel, Author, Tag


class AuthorContextMixin(ContextMixin):
    author_model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorContextMixin, self).get_context_data(**kwargs)
        context["author"] = self.author_model.objects.all()[0]
        return context


class SiteContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(SiteContextMixin, self).get_context_data(**kwargs)
        context["site"] = Site.objects.all()[0]
        return context


class BlogIndexView(
    AuthorContextMixin,
    SiteContextMixin,
    generic.ListView
):
    template_name = "blog/blog_index.html"
    model = BlogPostModel

    POSTS_PER_PAGE = 3

    def get_queryset(self):
        self.validate_correct_page()
        return self.model.objects.order_by("-posted_at")[
            self.get_starting_index():self.get_ending_index()]

    def get_context_data(self, **kwargs):
        self.validate_correct_page()
        context = super(BlogIndexView, self).get_context_data(**kwargs)
        context["has_older_posts"] = \
            self.get_ending_index() < self.get_amount_posts()
        context["has_newer_posts"] = self.get_starting_index() > 0
        context["page"] = self.kwargs.get("page")
        return context

    def validate_correct_page(self):
        if self.get_page() < 1:
            raise Http404
        if self.get_starting_index() > self.get_amount_posts():
            raise Http404

    def get_page(self):
        return int(self.kwargs.get("page"))

    def get_amount_posts(self):
        return self.model.objects.count()

    def get_starting_index(self):
        return (self.get_page() - 1) * self.POSTS_PER_PAGE

    def get_ending_index(self):
        return self.get_starting_index() + self.POSTS_PER_PAGE


class BlogPostDetail(
    AuthorContextMixin,
    SiteContextMixin,
    generic.DetailView,
):
    template_name = "blog/blogpost.html"
    context_object_name = "blogpost"
    model = BlogPostModel


class ArchiveView(
    AuthorContextMixin,
    generic.TemplateView,
):
    template_name = "blog/archive.html"

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)

        archive = OrderedDict()

        posted_at_values = \
            BlogPostModel.objects.order_by("-posted_at") \
                .values_list("posted_at", flat=True)

        # Make sure values are unique and ordered from high value to lower.
        years = sorted(
            list(set(map(lambda posted_at: posted_at.year, posted_at_values))),
            reverse=True)

        for year in years:
            year_dic = OrderedDict()
            posted_at_year = \
                BlogPostModel.objects.filter(posted_at__year=year) \
                    .order_by("-posted_at") \
                    .values_list("posted_at", flat=True)
            months = sorted(list(
                set(map(lambda posted_at: posted_at.month, posted_at_year))),
                            reverse=True)

            for month in months:
                month_dic = OrderedDict()
                posted_at_year_month = \
                    BlogPostModel.objects.filter(posted_at__year=year) \
                        .filter(posted_at__month=month) \
                        .order_by("-posted_at") \
                        .values_list("posted_at", flat=True)
                days = sorted(list(set(map(lambda posted_at: posted_at.day,
                                           posted_at_year_month))),
                              reverse=True)

                for day in days:
                    blogposts_at_day = \
                        BlogPostModel.objects.filter(posted_at__year=year) \
                            .filter(posted_at__month=month) \
                            .filter(posted_at__day=day) \
                            .order_by("-posted_at")
                    month_dic[day] = list(blogposts_at_day)

                year_dic[month] = month_dic
            archive[year] = year_dic

        context["archive"] = archive
        context["test"] = BlogPostModel.objects.all()
        return context


class AboutView(
    generic.TemplateView,
    AuthorContextMixin,
):
    template_name = "blog/about.html"


class TagView(
    generic.ListView,
    AuthorContextMixin,
):
    model = Tag
    template_name = "blog/tags.html"
    context_object_name = "tags"


    

