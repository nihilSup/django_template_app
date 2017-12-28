from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings

from rango.models import Category
from rango.models import Page

def index(request):
    'index page dispatcher'
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {
        'categories': category_list,
        'url_about': reverse('about')
    }

    return render(request, 'rango/index.html', context=context_dict)
def about(request):
    'about page dispatcher'
    context_dict = {'index_url': reverse('index'),
                    'MEDIA_URL': settings.MEDIA_URL,
                   }
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, ctg_name_slug):
    context_dict = {}
    try:
        ctg = Category.objects.get(slug=ctg_name_slug)
        pages = Page.objects.filter(category=ctg)
        context_dict['pages'] = pages
        context_dict['category'] = ctg
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context_dict)
