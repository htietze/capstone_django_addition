from django.test import TestCase
from django.urls import reverse

from .models import Place

# Create your tests here.

class TestHomePage(TestCase):

    def test_load_home_page_shows_empty_list_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')

class TestWishList(TestCase):
    fixtures = ['test_places']

    def test_view_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestEmptyVisitedPage(TestCase):
    
    def test_load_visited_page_message_for_empty_list(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')

class TestVisitedPage(TestCase):
    fixtures = ['test_places']

    def test_visited_contains_only_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')

        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')

class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place_to_wishlist(self):

        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        # what data used to populate template?
        response_places = response.context['places']
        # should be 1
        self.assertEqual(1, len(response_places))
        tokyo_response = response_places[0]

        # expect this data to be in the base, use get() to get data with
        # the values expected. throws exception if no data, or more than 1 row
        # throwing exception causes test to fail
        tokyo_in_database = Place.objects.get(name='Tokyo', visited=False)

        # is the data used to render the template same as data in db?
        self.assertEqual(tokyo_in_database, tokyo_response)

class TestVisitPlace(TestCase):
    fixtures = ['test_places']

    def test_visit_place(self):

        # visit place pk 2, new york
        visit_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visit_place_url, follow=True)

        # check template
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # no ny in response
        self.assertNotContains(response, 'New York')

        # is new york visited?
        new_york = Place.objects.get(pk=2)

        self.assertTrue(new_york.visited)

    def test_visit_non_existent_place(self):

        # visit place with bad pk
        visit_place_url = reverse('place_was_visited', args=(200, ))
        response = self.client.post(visit_place_url, follow=True)
        self.assertEqual(404, response.status_code) # not found