from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row_text for row in rows])
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Loads the Homepage
        self.browser.get('http://localhost:8000')

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

        #User types feathers into the text box and hits enter
        inputbox.send_keys('1: Buy feathers')
        inputbox.send_keys(Keys.ENTER)

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

        #does it remember the list?
        #the site generates a random URL
        #xplanitory text
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
