from django.shortcuts import render
from django.http import HttpResponse
from .models import Parent

def Guardian(request):
    query_set = Parent.objects.all()
    for parent in query_set:
        print(parent)
    return HttpResponse("Hello world")

# Create your views here.
