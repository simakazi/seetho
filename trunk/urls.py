# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import os.path
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
PROJECT_ROOT = os.path.dirname(__file__)

urlpatterns = patterns('',
 (r'^$','reader.views.index'),
 (r'^search/(.*)$','reader.views.search'),
 (r'^topic/(\d*)$','reader.views.list_topic'),
 (r'^start_topic/$','reader.views.start_topic'),
 (r'^add_comment/$','reader.views.add_comment'),
 (r'^purge_group/$','reader.views.purge_group'),
 (r'^create_group/$','reader.views.create_group'),
 (r'^groups/$','reader.views.list_groups'),
 (r'^unsubscribe_group/(\d*)$','reader.views.unsubscribe_group'),
 (r'^subscribe_group/(\d*)$','reader.views.subscribe_group'),
 (r'^group/(\d+)/pulls$','reader.views.list_group_pulls'),
 (r'^group/(\d+)/user/(\d+)$','reader.views.list_group_user'),
 (r'^group/(\d+)/users$','reader.views.list_group_users'),
 (r'^group/(\d+)/topics$','reader.views.list_group_topics'),
 (r'^group/(\d+)$','reader.views.list_group'),
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
