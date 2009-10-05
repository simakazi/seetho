#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management import setup_environ
import sys
import os
import time
from datetime import datetime
import feedparser

sys.path.append(os.path.abspath("../"))
import settings
setup_environ(settings)
from reader.models import Feed,Entry
sys.path.pop()

q=Feed.objects.all()[0]
print q
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
    q.last_cheked=datetime.now()
    q.save()
    count=0
    print len(E),"feeds found."
    for e in E:
	if not (q.entry_set.filter(native_id=e.id)):
	    en=Entry(native_id=e.id,title=e.title,summary=e.description,url=e.link,feed=q,downloaded=datetime.utcfromtimestamp(time.mktime(e.updated_parsed)))
	    en.save()
	    count+=1
    print len(E)-count,"of them are already in db"
