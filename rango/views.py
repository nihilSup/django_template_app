'application views(controllers)'
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page, UserProfile
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

@login_required
def register_profile(request):
    'registration controller, works both for get and post'
    if request.method == 'POST':
        #get posted data
        profile_form = UserProfileForm(data=request.POST)
        #check whether it is valid
        if profile_form.is_valid():
            #update profile after commiting user to avoid integrity problems
            user_prof = profile_form.save(commit=False)
            user_prof.user = request.user
            if 'picture' in request.FILES:
                user_prof.picture = request.FILES['picture']
            user_prof.save()
            return redirect('index')
        else:
            print(profile_form.errors)
    else:
        profile_form = UserProfileForm()

    return render(
        request,
        'rango/profile_registration.html',
        {
            'form': profile_form,
        }
    )

@login_required
def show_profile(request, username):
    'view and edit profile logic'
    context_dict = {'username': username}
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    context_dict['username'] = user.username
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    context_dict['profile'] = user_profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid:
            form.save(commit=True)
            return redirect('show_profile', username)
    else:
        form = UserProfileForm({
            'website': user_profile.website,
            'picture': user_profile.picture
        })
        context_dict['form'] = form

    return render(request, 'rango/profile.html', context_dict)

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

def track_url(request):
    'url tracking handler'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            url = page.url
            return redirect(url)

    return redirect('index')

@login_required
def like_category(request):
    'like button server side handler'
    if request.method == 'GET':
        ctg_id = request.GET['ctg_id']
        likes = 0
        if ctg_id:
            category = Category.objects.get(id=ctg_id)
            if category:
                category.likes += 1
                category.save()
                likes = category.likes
        return HttpResponse(likes)

def get_ctg_list(starts_with='', max_results=0):
    'returns list of categories which starts with supplied prefix'
    ctg_list = []
    if starts_with:
        ctg_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(ctg_list) > max_results:
            ctg_list = ctg_list[:max_results]

    return ctg_list

def suggest_category(request):
    'category filter controller'
    ctgs = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    ctgs = get_ctg_list(starts_with, 8)

    return render(request, 'rango/ctgs.html', {'ctgs': ctgs})
