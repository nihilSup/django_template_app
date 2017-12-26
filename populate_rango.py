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
         'url':'http://docs.python.org/2/tutorial/'},
        {'title':'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/'},
        {'title':'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/'}
    ]

    django_pages = [
        {'title':'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/1.9/intro/tutorial01/'},
        {'title':'Django Rocks',
         'url':'http://www.djangorocks.com/'},
        {'title':'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/'}
    ]

    other_pages = [
        {'title':'Bottle',
         'url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask',
         'url':'http://flask.pocoo.org'}
    ]

    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}
    }

    for cat, cat_data in cats.items():
        ctg = add_ctg(cat, cat_data['views'], cat_data['likes'])
        for page in cat_data['pages']:
            add_page(ctg, page['title'], page['url'])

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