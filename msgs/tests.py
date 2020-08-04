from django.test import TestCase

from msgs.views import home_page

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_post_request(self):
        response = self.client.post('/', data={'msg_text': 'A new message'})
        self.assertIn('A new message', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
        
                        

    


