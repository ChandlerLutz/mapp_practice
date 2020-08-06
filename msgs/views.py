from django.shortcuts import redirect, render
from msgs.models import Msg

def home_page(request):
    if request.method == "POST":
        Msg.objects.create(text=request.POST['msg_text'])
        return redirect('/')

    msgs = Msg.objects.all()
    return render(request, 'home.html', {'msgs': msgs})
