from django.test import TestCase

# Create your tests here.
from rango.models import Category, Page
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should results True for categories
        where views are zero or positive
        """

        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add
        a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

class IndexViewTests(TestCase):

    def test_index_view_with_no_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        Check to make sure that the index has categories displayed
        """

        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)

class PageMethodTests(TestCase):
    def test_ensure_last_visit_or_first_visit_not_in_future(self):
        """
        ensure that the last_visti and first_visit are not in future.
        """
        cat = add_cat('test', 1, 1)
        page = Page(category=cat, title='test_page', url='http://www.example.com', views=1, first_visit=datetime.now()+timedelta(hours=6), last_visit=datetime.now()+timedelta(hours=6))
        page.save()
        self.assertEqual((page.first_visit <= datetime.now()), True)
        self.assertEqual((page.last_visit <= datetime.now()), True)
