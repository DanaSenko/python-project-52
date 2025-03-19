from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    a = None
    a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")

class IndexView(TemplateView):
    template_name = "index.html"
