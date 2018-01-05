'app specific urls'

from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<ctg_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<ctg_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.show_profile, name='show_profile'),
    url(r'^like/$', views.like_category, name='like_category'),
    url(r'^suggest/$', views.suggest_category, name='suggest_category'),
]
