from django.shortcuts import render
from .models import Parent


def Guardian(request):
    query_set = Parent.objects.all()
    for parent in query_set:
        print(parent)
    return render(request, 'index.html', {'parents': "Ilyas"})
# Create your views here.
