# functional_tests/tests.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_send_a_message(self):
        # Edith heard about a cool new messaging app.
        # The app brings the mail of yesteryear to the internet.
        # Edith's mail is delivered everyday at 5. She gets
        # her mail, reads, respnds, and then lives her life.
        #browser.get(self.live_server_url)
        self.browser.get("http://localhost:8000/")


        # She notices a page title and header mentions the message app name 
        self.assertIn('Mapp', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Mapp Messages', header_text)

        # She is invited to send a message right away
        inputbox = self.browser.find_element_by_id('id_new_message')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Send a message'
        )

        # She types, "I want to buy peacock feathers" into a text box.
        # Edith's hobby is fly fishing
        inputbox.send_keys('I want to buy peacock feathers')
        

        # When she hits enter, the page updates and now the page
        # has a message from edith that says, "I want to buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_message_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == 'I want to buy peacock feathers' for row in rows),
            'New message did not appear in table'
        )

        
        # There is stil a text box inviting her to send another message
        # She types, "I will then use the peacock feathers to make a fly"
        self.fail('Finish the Test')
        
        # The page udpates again, and now there are two messages from edith


if __name__ == '__main__':
    unittest.main(warnings='ignore')
