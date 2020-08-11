from django.shortcuts import redirect, render
from msgs.models import Msg, Thread

def home_page(request):
    return render(request, 'home.html')

def view_thread(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    return render(request, 'thread.html', {'thread': thread})

def new_thread(request):
    thread = Thread.objects.create()
    Msg.objects.create(text=request.POST['msg_text'], thread=thread)
    return redirect(f'/threads/{thread.id}/')


def add_msg(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    Msg.objects.create(text=request.POST['msg_text'], thread=thread)
    return redirect(f'/threads/{thread_id}/')

    
