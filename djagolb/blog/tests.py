from collections import OrderedDict
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from django.utils.datetime_safe import datetime
from .models import BlogPostModel


def create_dummy_blogpost(slug, save=True):
    dummy_blogpost = BlogPostModel(
        slug=slug,
        md_content="Just testing some blogpost",
        title="Test Blogpost"
    )

    if save:
        dummy_blogpost.save()

    return dummy_blogpost


def create_dummy_blogpost_posted_at_datetime(slug, datetime_instance):
    dummy_blogpost = create_dummy_blogpost(slug)
    dummy_blogpost.posted_at = \
        timezone.make_aware(datetime_instance,
                            timezone.get_default_timezone())
    dummy_blogpost.save()
    return dummy_blogpost


class BlogPostModelTest(TestCase):
    def test_is_edited_should_be_false_on_just_created_blogpost(self):
        right_now_blogpost = create_dummy_blogpost("rightnow")

        self.assertFalse(right_now_blogpost.is_edited())

        right_now_blogpost.delete()

    def test_is_edited_should_be_true_on_blogpost_created_one_min_ago(self):
        created_long_ago_blogpost = create_dummy_blogpost_posted_at_datetime(
            "one-min-ago", datetime.now() - timedelta(minutes=1))

        self.assertTrue(created_long_ago_blogpost.is_edited())

        created_long_ago_blogpost.delete()


class ArchiveViewTests(TestCase):
    def test_no_blogposts(self):
        resp = self.client.get(reverse("blog:archive"))
        self.assertEqual(resp.context["archive"], OrderedDict())

    def test_archive_with_one_blogpost(self):
        example_blogpost = create_dummy_blogpost_posted_at_datetime(
            "example", datetime(1990, 10, 20, 14, 20, 00)
        )

        resp = self.client.get(reverse("blog:archive"))
        archive_dic = resp.context["archive"]

        expected_archive_contents = \
            ((1990,
              (10,
               (20, [example_blogpost]),
              ),
             ),)

        self.assertEqual(archive_dic, self.expand_tuples_to_ordered_dic(
            expected_archive_contents))

        example_blogpost.delete()

    def test_archive_with_two_year_separated_blogposts(self):
        example_blogpost1 = create_dummy_blogpost_posted_at_datetime(
            "example", datetime(1990, 10, 20, 14, 20, 00)
        )
        example_blogpost2 = create_dummy_blogpost_posted_at_datetime(
            "example2", datetime(2004, 8, 10, 12, 00, 10)
        )

        resp = self.client.get(reverse("blog:archive"))
        archive_dic = resp.context["archive"]
        expected_archive_contents = \
            ((2004,
              (8,
               (10, [example_blogpost2])
              )
             ),
             (1990,
              (10,
               (20, [example_blogpost1]),
              ),
             ),
            )

        self.assertEqual(archive_dic, self.expand_tuples_to_ordered_dic(
            expected_archive_contents))

        example_blogpost1.delete()

    def expand_tuples_to_ordered_dic(self, tuples):
        """
        Simple function to create a ordered dict from tuples so tests can be
        written faster.
        """
        if len(tuples) == 1 and isinstance(tuples[0], list):
            return tuples[0]

        dic = OrderedDict()
        for tup in tuples:
            key, value = tup[0], tup[1:]
            if isinstance(value, tuple):
                dic[key] = self.expand_tuples_to_ordered_dic(value)
        return dic





