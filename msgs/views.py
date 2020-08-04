from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request, 'home.html', {
        'new_msg_text': request.POST.get('msg_text', ''), 
    })
