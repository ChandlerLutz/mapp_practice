from django.shortcuts import render
from django.http import HttpResponse

def home_page(response):
    return HttpResponse('<html><title>Mapp</title></html>')
