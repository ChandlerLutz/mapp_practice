from django.test import TestCase
from msgs.models import Msg 

from msgs.views import home_page

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_post_request(self):
        response = self.client.post('/', data={'msg_text': 'A new message'})
        self.assertIn('A new message', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
        
                        

class MsgModelTest(TestCase):

    def test_saving_and_retrieving_msgs(self):
        first_msg = Msg()
        first_msg.text = 'The first (ever) message'
        first_msg.save()

        second_msg = Msg()
        second_msg.text = 'Msg the second'
        second_msg.save()

        saved_msgs = Msg.objects.all()
        self.assertEqual(saved_msgs.count(), 2)

        first_saved_msg = saved_msgs[0]
        second_saved_msg = saved_msgs[1]
        self.assertEqual(first_saved_msg.text, 'The first (ever) message')
        self.assertEqual(second_saved_msg.text, 'Msg the second')
        
        
