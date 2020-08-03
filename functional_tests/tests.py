# functional_tests/tests.py
from selenium import webdriver
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

        # She is invited to send a message right away

        # She types, "I want to buy peacock feathers" into a text box.
        # Edith's hobby is fly fishing

        # When she hits enter, the page updates and now the page
        # has a message from edith that says, "I want to buy peacock feathers"
        
        # There is stil a text box inviting her to send another message

        # She types, "I will then use the peacock feathers to make a fly"
        
        # The page udpates again, and now there are two messages from edith


if __name__ == '__main__':
    unittest.main(warnings='ignore')
