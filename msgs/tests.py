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
        thread = Thread.objects.create()
        response = self.client.get(f'/threads/{thread.id}/')
        self.assertTemplateUsed(response, 'thread.html')

    def test_displays_only_items_for_that_thread(self):
        correct_thread = Thread.objects.create()
        Msg.objects.create(text='messagey 1', thread=correct_thread)
        Msg.objects.create(text='messagey 2', thread=correct_thread)
        other_thread = Thread.objects.create()
        Msg.objects.create(text='other msg 1', thread=other_thread)
        Msg.objects.create(text='other msg 2', thread=other_thread)

        response = self.client.get(f'/threads/{correct_thread.id}/')

        self.assertContains(response, 'messagey 1')
        self.assertContains(response, 'messagey 2')
        self.assertNotContains(response, 'other msg 1')
        self.assertNotContains(response, 'other msg 2')
        

    def test_displays_all_msgs(self):
        thread = Thread.objects.create()
        Msg.objects.create(text='messagey 1', thread=thread)
        Msg.objects.create(text='messagey 2', thread=thread)

        response = self.client.get(f'/threads/{thread.id}/')

        self.assertContains(response, 'messagey 1')
        self.assertContains(response, 'messagey 2')

    def test_passes_correct_list_to_template(self):
        other_thread = Thread.objects.create()
        correct_thread = Thread.objects.create()
        response = self.client.get(f'/threads/{correct_thread.id}/')
        self.assertEqual(response.context['thread'], correct_thread)
        
        

class NewThreadTest(TestCase):


    def test_can_save_a_POST_request(self):
        response = self.client.post('/threads/new', data={'msg_text': 'A new message'})

        self.assertEqual(Msg.objects.count(), 1)
        new_msg = Msg.objects.first()
        self.assertEqual(new_msg.text, 'A new message')

    def test_redirects_after_POST(self):
        response = self.client.post('/threads/new', data={'msg_text': 'A new message'})
        new_thread = Thread.objects.first()
        self.assertRedirects(response, f'/threads/{new_thread.id}/')

class NewMsgTest(TestCase):

    def test_can_save_a_POST_to_an_existing_thread(self):
        other_thread = Thread.objects.create()
        correct_thread = Thread.objects.create()

        self.client.post(
            f'/threads/{correct_thread.id}/add_msg',
            data={'msg_text': 'A new message for an existing thread'}
        )

        self.assertEqual(Msg.objects.count(), 1)
        new_msg = Msg.objects.first()
        self.assertEqual(new_msg.text, 'A new message for an existing thread')
        self.assertEqual(new_msg.thread, correct_thread)

    def test_redirects_to_thread_view(self):
        other_thread = Thread.objects.create()
        correct_thread = Thread.objects.create()

        response = self.client.post(
            f'/threads/{correct_thread.id}/add_msg',
            data={'msg_text': 'A new item for an existing thread'}
        )

        self.assertRedirects(response, f'/threads/{correct_thread.id}/')

        
            
            
