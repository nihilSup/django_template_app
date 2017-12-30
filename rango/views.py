from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings

from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm

def index(request):
    'index page dispatcher'
    category_list = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories': category_list,
        'pages': pages,
    }

    return render(request, 'rango/index.html', context=context_dict)
def about(request):
    'about page dispatcher'
    context_dict = {
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
    context_dict['back'] = reverse('index')

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    'add category controller'
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid:
            #save new (?) form to db
            ctg = form.save(commit=True)
            print(ctg, ctg.slug)

            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, ctg_name_slug):
    'add page controller'
    try:
        ctg = Category.objects.get(slug=ctg_name_slug)
    except Category.DoesNotExist:
        print(f"{ctg_name_slug} does not exist")
        ctg = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid:
            if ctg:
                page = form.save(commit=False)
                page.category = ctg
                page.views = 0
                page.save()
                print("Added new page:")
                print(page, page.title)

                return index(request)
        else:
            print(form.errors())

    return render(
        request,
        'rango/add_page.html',
        {
            'form': form,
            'ctg': ctg
        }
    )
