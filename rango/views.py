from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings

def index(request):
    'index page dispatcher'
    context_dict = {'about_url': reverse('about')}
    return render(request, 'rango/index.html', context=context_dict)
def about(request):
    'about page dispatcher'
    context_dict = {'index_url': reverse('index'),
                    'MEDIA_URL': settings.MEDIA_URL,
                   }
    return render(request, 'rango/about.html', context=context_dict)
