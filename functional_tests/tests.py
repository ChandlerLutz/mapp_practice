# functional_tests/tests.py
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_msg_table(self, row_text):
        table = self.browser.find_element_by_id('id_msg_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_send_a_message(self):
        # Edith heard about a cool new messaging app.
        # The app brings the mail of yesteryear to the internet.
        # Edith's mail is delivered everyday at 5. She gets
        # her mail, reads, respnds, and then lives her life.
        #browser.get(self.live_server_url)
        self.browser.get(self.live_server_url)


        # She notices a page title and header mentions the message app name 
        self.assertIn('Mapp', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Mapp Messages', header_text)

        # She is invited to send a message right away
        inputbox = self.browser.find_element_by_id('id_new_msg')
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
        self.check_for_row_in_msg_table('1: I want to buy peacock feathers')
        
        
        # There is stil a text box inviting her to send another message
        # She types, "I will then use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_msg')
        inputbox.send_keys('I will then use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # The page udpates again, and now there are two messages from edith
        self.check_for_row_in_msg_table('1: I want to buy peacock feathers')
        self.check_for_row_in_msg_table('2: I will then use peacock feathers to make a fly')

        # Edith wonders whether the site will remember her list. Then
        # she sees that the site has generated a unique URL for her --
        ##there is some explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to list is still there
