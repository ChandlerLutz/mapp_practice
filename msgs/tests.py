from django.test import TestCase
from msgs.models import Msg 

from msgs.views import home_page

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'msg_text': 'A new message'})

        self.assertEqual(Msg.objects.count(), 1)
        new_msg = Msg.objects.first()
        self.assertEqual(new_msg.text, 'A new message')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'msg_text': 'A new message'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/threads/the-only-thread-in-the-world/')
        

    def test_only_saves_messages_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Msg.objects.count(), 0)
                        

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
        
        
class ThreadViewTest(TestCase):

    def test_uses_thread_template(self):
        response = self.client.get('/threads/the-only-thread-in-the-world/')
        self.assertTemplateUsed(response, 'thread.html')

    def test_displays_all_items(self):
        Msg.objects.create(text='thready 1')
        Msg.objects.create(text='thready 2')

        response = self.client.get('/threads/the-only-thread-in-the-world/')

        self.assertContains(response, 'thready 1')
        self.assertContains(response, 'thready 2')
