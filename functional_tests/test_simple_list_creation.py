from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Loads the Homepage
        self.browser.get(self.server_url)

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
        self.browser.get(self.server_url)
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
