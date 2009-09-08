# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from models import Feed,Entry,News
from forms import FeedForm
from reader.feedget import feedfinder,feedparser
from datetime import datetime
import time

@login_required
def add_feed(request):
    if request.method == 'POST': 
        form = FeedForm(request.POST)
        if form.is_valid():
	    rss=feedfinder.feed(form.cleaned_data['url'])
	    if not (Feed.objects.filter(url=rss)):
		feed=Feed(url=rss,last_cheked="2009-01-01 00:00")
		feed.save()
            return HttpResponseRedirect('/')
    else:
        form = FeedForm()

    return render_to_response('feeds.html', {
        'feedform': form,'feeds':[]
    })

def index(request):
    if (request.user.is_authenticated()):
	return list_feeds(request)
    else:
	return render_to_response('index-anonymous.html',{
	    'news':News.objects.all()[:15]
	})

def list_feeds(request):
    for feed in Feed.objects.all():
	check_feed(feed)
    return render_to_response('feeds.html', {
	'feedform':FeedForm(),'feeds':Feed.objects.all(),'user':request.user
    })



def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")


def check_feed(q):
    if True:#q.last_cheked<time.time()-5 or q.last_cheked==-1:
	R=feedparser.parse(q.url,modified=q.last_cheked.utctimetuple())
	if q.title=="":
	    try:
		q.title=R.feed.title
	    except:
		q.title=q.url
	    try:
		q.subtitle=R.feed.subtitle
	    except:
		q.subtitle=""
	    try:
		q.link=R.feed.link
	    except:
		q.link=q.url
	    q.save()
	E=R.entries
	q.last_cheked=datetime.now().isoformat()
	count=0
	for e in E:
	    if not (q.entry_set.filter(native_id=e.id)):
		en=Entry(native_id=e.id,title=e.title,summary=e.description,url=e.link,feed=q)
		en.save()
		print en.url
		print en.title
		print
		count+=1
	print len(E)-count,"of them are already in db"