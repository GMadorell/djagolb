from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed
from.models import BlogPostModel


class BlogRssFeed(Feed):
    title = "Djagolb blogposts feed"
    link = ""
    description = "A feed with Djagolb blogposts"

    def items(self):
        return BlogPostModel.objects.order_by("-posted_at")[:5]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return reverse("blog:blogpost", kwargs={"slug": str(item.slug)})

    def item_description(self, item):
        return item.title


class BlogAtomFeed(BlogRssFeed):
    feed_type = Atom1Feed
    subtitle = BlogRssFeed.description

