from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):
        #Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        #She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        #She starts a new list  and sees the input is nicely centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row_text for row in rows])
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Loads the Homepage
        self.browser.get(self.live_server_url)

        #Checks for 'To-Do' in header and page title.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #User attemps to add a to-do item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #User(edith) types feathers into the text box and hits enter
        #We are taken to a new URL and the string appears as a item in the list.
        inputbox.send_keys('1: Buy feathers')
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #The page updates and lists "1: Buy feathers" as a to-do item
        self.check_for_row_in_list_table('1: Buy feathers')

        #There is still a text box inviting us to add another item. 
        #We enter use feathers to make a fly.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('2: Use feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        #The Page updates again, and now shows both items on the list:
        self.check_for_row_in_list_table('1: Buy feathers')
        self.check_for_row_in_list_table('2: Use feathers to mak a fly')

        #Now a new user, Francis, comes along to the site.

        ##We use a new browser session to make sure that no information
        ##of Edith's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Francis visits the home page. 
        #There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #Francis starts a new list by entering a new item.
        #He is less interesting than Edith
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #Again, There's no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertIn('Buy milk', page_text)

