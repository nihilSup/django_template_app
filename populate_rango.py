import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    'populate rango app'
    python_pages = [
        {'title':'Official Python Tutorial',
         'url':'http://docs.python.org/2/tutorial/',
         'views': 45},
        {'title':'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/',
         'views': 97},
        {'title':'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views': 32}
    ]

    django_pages = [
        {'title':'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/1.9/intro/tutorial01/',
         'views': 16},
        {'title':'Django Rocks',
         'url':'http://www.djangorocks.com/',
         'views': 56},
        {'title':'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/',
         'views': 77}
    ]

    other_pages = [
        {'title':'Bottle',
         'url':'http://bottlepy.org/docs/dev/',
         'views': 13},
        {'title':'Flask',
         'url':'http://flask.pocoo.org',
         'views': 56}
    ]

    pascal_pages = [
        {'title':'FastPlaz',
         'url':'http://www.fastplaz.com',
         'views': 13},
    ]

    perl_pages = [
        {'title':'PragmaticPerl',
         'url':'http://pragmaticperl.com',
         'views': 13},
    ]

    php_pages = [
        {'title':'Php SU',
         'url':'http://www.php.su',
         'views': 13},
    ]

    prolog_pages = [
        {'title':'SWI Prolog',
         'url':'http://www.swi-prolog.org',
         'views': 13},
    ]

    post_script_pages = [
        {'title':'Adobe post script',
         'url':'http://www.adobe.com/products/postscript.html',
         'views': 13},
    ]

    programming_pages = [
        {'title':'Habr',
         'url':'https://habrahabr.ru',
         'views': 13},
    ]

    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16},
        'Pascal': {'pages': pascal_pages, 'views': 0, 'likes': 0},
        'Perl': {'pages': perl_pages, 'views': 0, 'likes': 0},
        'PHP': {'pages': php_pages, 'views': 0, 'likes': 0},
        'Prolog': {'pages': prolog_pages, 'views': 0, 'likes': 0},
        'PostScript': {'pages': post_script_pages, 'views': 0, 'likes': 0},
        'Programming': {'pages': programming_pages, 'views': 0, 'likes': 0},
    }

    for cat, cat_data in cats.items():
        ctg = add_ctg(cat, cat_data['views'], cat_data['likes'])
        for page in cat_data['pages']:
            add_page(ctg, page['title'], page['url'], page['views'])

    # Print added ctgrs
    for ctg in Category.objects.all():
        for page in Page.objects.filter(category=ctg):
            print('- {0} - {1}'.format(str(ctg), str(page)))

def add_page(cat, title, url, views=0):
    'constructs and adds page to db, returns constructed page'
    page = Page.objects.get_or_create(category=cat, title=title)[0]
    page.url = url
    page.views = views
    page.save()
    return page

def add_ctg(name, views=0, likes=0):
    'builds category, adds to db and returns it'
    ctg = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    ctg.save()
    return ctg

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
