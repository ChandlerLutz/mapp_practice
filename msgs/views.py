from django.shortcuts import redirect, render
from msgs.models import Msg, Thread

def home_page(request):
    return render(request, 'home.html')

def view_thread(request):
    msgs = Msg.objects.all()
    return render(request, 'thread.html', {'msgs': msgs})

def new_thread(request):
    thread = Thread.objects.create()
    Msg.objects.create(text=request.POST['msg_text'], thread=thread)
    return redirect('/threads/the-only-thread-in-the-world/')

    
