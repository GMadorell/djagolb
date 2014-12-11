from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.utils.datetime_safe import datetime
from .models import BlogPostModel


class BlogPostModelTest(TestCase):

    def setUp(self):
        self.basic_blogpost = BlogPostModel(
            slug="test-blogpost",
            md_content="Just testing some blogpost",
            title="Test Blogpost"
        )
        self.basic_blogpost.save()

    def test_is_edited_should_be_false_on_just_created_blogpost(self):
        right_now_blogpost = BlogPostModel(
            slug="rightnow-blogpost",
            md_content="Just testing some blogpost",
            title="Right now"
        )
        right_now_blogpost.save()

        self.assertFalse(right_now_blogpost.is_edited())

        right_now_blogpost.delete()

    def test_is_edited_should_be_true_on_blogpost_created_one_min_ago(self):
        created_long_ago_blogpost = BlogPostModel(
            slug="rightnow-blogpost",
            md_content="Just testing some blogpost",
            title="Right now",
        )
        created_long_ago_blogpost.save()
        created_long_ago_blogpost.posted_at = \
            timezone.make_aware(datetime.now() - timedelta(minutes=1),
                                timezone.get_default_timezone())

        self.assertTrue(created_long_ago_blogpost.is_edited())

        created_long_ago_blogpost.delete()