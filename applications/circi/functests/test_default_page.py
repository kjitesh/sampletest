from functional_tests import FunctionalTest, BASE_URL

class TestHomePage (FunctionalTest):

    def test_can_view_circi_home_page(self):

        # open browser and go to welcome app
        self.browser.get(BASE_URL + '/circi/')

        # Check if hello world in page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Hello World', body.text)

class TestListingPage (FunctionalTest):

    def test_can_view_listing_page(self):

        # open browser and go to welcome app
        self.browser.get(BASE_URL + '/circi/default/show_records')

        # Check if hello world in page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Records are as follows:', body.text)
