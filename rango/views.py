'application views(controllers)'
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
    'index page dispatcher'
    category_list = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories': category_list,
        'pages': pages,
    }
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response

def get_server_cookie(request, cookie, def_value=None):
    'helper to get server cookie'
    val = request.session.get(cookie)
    return val if val else def_value

def visitor_cookie_handler(request):
    'adds visits to request session'
    visits = int(get_server_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def about(request):
    'about page dispatcher'
    context_dict = {
        'MEDIA_URL': settings.MEDIA_URL,
        'visits': get_server_cookie(request, 'visits', '1')
    }
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, ctg_name_slug):
    'show ctg controller'
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

@login_required
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

@login_required
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

def register(request):
    'registration controller, works both for get and post'
    registered = False
    if request.method == 'POST':
        #get posted data
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        #check whether it is valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #set_password hashes plain password
            user.set_password(user.password)
            user.save()

            #update profile after commiting user to avoid integrity problems
            user_prof = profile_form.save(commit=False)
            user_prof.user = user
            if 'picture' in request.FILES:
                user_prof.picture = request.FILES['picture']

            user_prof.save()
            registered = True
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        'rango/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        }
    )

def login_user(request):
    'login logic'
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=user, password=password)

        build_context = lambda msg: {'err_msg': msg}

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                err = """Account is deactivated. Activate it and try again"""
                return render(request, 'rango/login.html', build_context(err))
        else:
            print(f'Invalid username/password: {user} / {password}')
            err = 'Invalid login details supplied'
            return render(request, 'rango/login.html', build_context(err))
    else:
        return render(request, 'rango/login.html', {})

@login_required
def logout_user(request):
    'logout logic'
    logout(request)
    return HttpResponseRedirect(reverse('index'))
