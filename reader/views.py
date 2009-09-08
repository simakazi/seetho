# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from models import Feed,Entry,News,Pull,FeedFilterPair,UserPull,Filter,PullEntry
from forms import FeedForm
from reader.feedget import feedfinder,feedparser
from datetime import datetime
import time
from django.db.models import Q

@login_required
def add_feed(request):
    if request.method == 'POST': 
        form = FeedForm(request.POST)
        if form.is_valid():
	    feed_url=form.cleaned_data['feed_url']
	    feed_cheked=form.cleaned_data['feed_cheked']
	    filter_must=form.cleaned_data['filter_must']
	    filter_may=form.cleaned_data['filter_may']
	    filter_not=form.cleaned_data['filter_not']
	    pull_title=form.cleaned_data['pull_title']
	    pull_id=form.cleaned_data['pull_id']
	    print filter_must,filter_may,filter_not
	    if not feed_cheked:
		feed_url=feedfinder.feed(feed_url)
	    feed=Feed.objects.filter(url=feed_url)
	    if not (feed):
		feed=Feed(url=feed_url,last_cheked="2009-01-01 00:00")
		feed.save()
	    else:
		feed=feed[0]
	    
	    pull=0
	    if (pull_id!=-1):
		pull=Pull.objects.get(id=pull_id)
	    else:
		pull=Pull(title=pull_title)
		pull.save()
	    
	    pair=FeedFilterPair(pull=pull,feed=feed,user=request.user,last_cheked="2009-01-01 00:00",title="")
	    pair.save()
	    
	    for q in [(1,filter_must),(2,filter_may),(3,filter_not)]:
		for w in map(lambda x:x.strip(),q[1].split(",")):
		    if w!="":
			filter1=Filter(type=q[0],value=w,pair=pair)
			filter1.save()
	    if pull_id==-1:
		up=UserPull(user=request.user,pull=pull)
		up.save()

            return HttpResponseRedirect('/')
    else:
        form = FeedForm()

    return render_to_response('newfeed.html', {
        'feedform': form,'feeds':[]
    })

def find_feed(request):
    if request.method=='POST':
	url=request.POST["url"]
	print url
	url=feedfinder.feed(url)
	print url
	return HttpResponse(url)
    else:
	return "Error"

def suggest_feed(request):
    if request.method=='POST':
	control_id=request.POST['control_id']
	div_id=request.POST['div_id']
	first_chars=request.POST['first_chars']
	L=map(lambda x:x.url,Feed.objects.filter(url__startswith=first_chars)[:5])
	return render_to_response("suggest_widget.html",{"L":L,"control_id":control_id,"div_id":div_id})
    else:
	print "VERYVERYBAD!"
	return "Error"

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
    P=Pull.objects.filter(Q(userpull__user=request.user)|Q(group__users=request.user))
    for p in P:
	for q in FeedFilterPair.objects.filter(pull=p):
	    for e in Entry.objects.filter(feed=q.feed).exclude(pullentry__pull=p):
		flag1=True
		flag2=False
		flag2on=False
		flag3=True
		for f in Filter.objects.filter(pair=q):
		    if (f.type==1 and e.summary.count(f.value)==0):
			flag1=False
		    elif (f.type==2 and e.summary.count(f.value)==0):
			flag2on=True
		    elif (f.type==2):
			flag2on=True
			flag2=True
		    elif (f.type==3 and e.summary.count(f.value)!=0):
			flag3=False
		if (flag3 and flag1 and (flag2 or (flag2==flag2on))):
		    ep=PullEntry(pull=p,entry=e)
		    ep.save()
    e=Entry.objects.filter(pullentry__pull__userpull__user=request.user)
    print P
    return render_to_response('newfeed.html', {
	'feedform':FeedForm(),'pulls':P,'entries':e,'user':request.user
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