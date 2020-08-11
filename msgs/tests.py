from django.test import TestCase
from msgs.models import Msg, Thread

from msgs.views import home_page

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ThreadAndMsgModelTest(TestCase):

    def test_saving_and_retrieving_msgs(self):
        thread = Thread()
        thread.save()
        
        first_msg = Msg()
        first_msg.text = 'The first (ever) message'
        first_msg.thread = thread
        first_msg.save()

        second_msg = Msg()
        second_msg.text = 'Msg the second'
        second_msg.thread = thread
        second_msg.save()

        saved_thread = Thread.objects.first()
        self.assertEqual(saved_thread, thread)

        saved_msgs = Msg.objects.all()
        self.assertEqual(saved_msgs.count(), 2)

        first_saved_msg = saved_msgs[0]
        second_saved_msg = saved_msgs[1]
        self.assertEqual(first_saved_msg.text, 'The first (ever) message')
        self.assertEqual(first_saved_msg.thread, thread)
        self.assertEqual(second_saved_msg.text, 'Msg the second')
        self.assertEqual(second_saved_msg.thread, thread)
        
        
class ThreadViewTest(TestCase):

    def test_uses_thread_template(self):
        response = self.client.get('/threads/the-only-thread-in-the-world/')
        self.assertTemplateUsed(response, 'thread.html')

    def test_displays_all_items(self):
        thread = Thread.objects.create()
        Msg.objects.create(text='thready 1', thread=thread)
        Msg.objects.create(text='thready 2', thread=thread)

        response = self.client.get('/threads/the-only-thread-in-the-world/')

        self.assertContains(response, 'thready 1')
        self.assertContains(response, 'thready 2')

class NewThreadTest(TestCase):


    def test_can_save_a_POST_request(self):
        response = self.client.post('/threads/new', data={'msg_text': 'A new message'})

        self.assertEqual(Msg.objects.count(), 1)
        new_msg = Msg.objects.first()
        self.assertEqual(new_msg.text, 'A new message')

    def test_redirects_after_POST(self):
        response = self.client.post('/threads/new', data={'msg_text': 'A new message'})
        self.assertRedirects(response, '/threads/the-only-thread-in-the-world/')
