from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render
from .models import Parent


def Guardian(request):
   query_set = Parent.objects.filter(id__lt=10).order_by('first_name')
   return render(request, 'index.html', {'name': "Ilyas", 'parents' : query_set})
# Create your views here.
