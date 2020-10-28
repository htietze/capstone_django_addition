from selenium.webdriver.chrome.webdriver import WebDriver

from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):

    # this bit doesn't make a lot of sense.

    # setup and teardown classes like usual, super() declares what the method is?
    # setup brings in the webdriver, and then a 10ms wait time to give it time to start I assume
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    # this caused issues with my mac, live_server_url was causing errors but not causing test failures.
    # selenium gets the web page using the live_server_url which would lead to the main page I think
    def test_title_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)


class AddPlacesTest(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    # also had errors here
    # selenium finds html elements with their IDs and checks the element contents
    # this lets it find the button whichi it can click to add info it provides
    # then does another check to make sure that data is in the refreshed webpage html again.
    def test_add_new_place(self):
        self.selenium.get(self.live_server_url)
        input_name = self.selenium.find_element_by_id('id_name')
        input_name.send_keys('Denver')

        add_button = self.selenium.find_element_by_id('add-new-place')
        add_button.click()

        denver = self.selenium.find_element_by_id('place-name-5')
        self.assertEqual('Denver', denver.text)

        self.assertIn('Denver', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)
