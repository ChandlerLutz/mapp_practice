# functional_tests/tests.py
import os # to help with getting environment variables 
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_msg_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_msg_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_send_a_message_for_one_user(self):
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
        self.wait_for_row_in_msg_table('1: I want to buy peacock feathers')
        
        # There is stil a text box inviting her to send another message
        # She types, "I will then use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_msg')
        inputbox.send_keys('I will then use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        
        # The page udpates again, and now there are two messages from edith
        self.wait_for_row_in_msg_table('1: I want to buy peacock feathers')
        self.wait_for_row_in_msg_table('2: I will then use peacock feathers to make a fly')

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_message_threads_at_different_urls(self):
        # Edith starts a new thread
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_msg')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_msg_table('1: Buy peacock feathers')

        # She notices that her message thread has a unique URL
        edith_thread_url = self.browser.current_url
        self.assertRegex(edith_thread_url, '/threads/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's message thread
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        
        # Frances starts a new msg thread. He is less interesting than edith
        inputbox = self.browser.find_element_by_id('id_new_msg')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_msg_table('1: Buy milk')

        # Frnaces gets his own unique URL
        francis_thread_url = self.browser.current_url
        self.assertRegex(francis_thread_url, '/threads/.+')
        self.assertNotEqual(francis_thread_url, edith_thread_url)

        # Again, there is no trace of Edith's thread
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        
        
        # Satisfied, they both go back to sleep.


    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_msg')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new thread and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_msg_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_msg')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512, 
            delta=10
        )
        

        # Edith wonders whether the site will remember her messages. Then
        # she sees that the site has generated a unique URL for her --
        ##there is some explanatory text to that effect.


        # She visits that URL - her to list is still there
