# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import os.path
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
PROJECT_ROOT = os.path.dirname(__file__)

urlpatterns = patterns('',
 (r'^$','reader.views.index'),
 (r'^create_pull/$','reader.views.create_pull'),
 (r'^clean_pull/$','reader.views.clean_pull'),
 (r'^purge_pull/$','reader.views.purge_pull'),
 (r'^pulls/$','reader.views.list_pulls'),
 (r'^pull/(\d*)$','reader.views.list_pull_entries'),
 (r'^find_feed/$','reader.views.find_feed'),
 (r'^suggest_feed/$','reader.views.suggest_feed'),
 (r'^add_feed/$','reader.views.add_feed'),
 (r'^openid/', include('django_openid_auth.urls')),
 (r'^logout/$', 'reader.views.logout'),
 (r'^.*img/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(PROJECT_ROOT,'media/img')}),
 (r'^.*css/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(PROJECT_ROOT,'media/css')}),
 (r'^.*js/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(PROJECT_ROOT,'media/js')}),

    # Example:
    # (r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/(.*)', admin.site.root),
)
