#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedfinder
import feedparser
import sys
import time
import model


def checkfeed(feedurl):
    feed=model.Feed(feedurl,-1)
    q=model.add_or_get_feed(feed)
    if q.last_cheked<time.time()-5 or q.last_cheked==-1:
	E=feedparser.parse(feedurl,modified=time.localtime(q.last_cheked)).entries
	q=model.update_feed_time(q)
	print len(E),"new entries in feed",feedurl,"..."
	count=0
	session=model.Session()
	entries=session.query(model.Entry.native_id).filter(model.Entry.feed_id==q.id).all()
	#print urls
	for e in E:
	    en=model.Entry(e.id,e.title,e.summary,e.link)
	    if not ((en.native_id,) in entries):#(en.url,) in urls:
		en.feed_id=q.id
		session.add(en)
		print en.url
		print en.title
		print
		count+=1
	session.commit()
	print len(E)-count,"of them are already in db"
 

def main():
    print "Checking DB..."
    #check_db()
    print "Ok"
    
    if len(sys.argv)>1:
      for w in sys.argv[1:]:
        print "Check site",w
        feedurl=feedfinder.feed(w)
        if (feedurl==""):
          print "No feeds found, sorry"
        else:
	    feed=model.Feed(feedurl,-1)
	    q=model.add_or_get_feed(feed)
	    if q.lastcheked<time.time()-5 or q.lastcheked==-1:
		print q.lastcheked,time.localtime(q.lastcheked)
		E=feedparser.parse(feedurl,modified=time.localtime(q.lastcheked)).entries
		q=model.update_feed_time(q)
		print len(E),"new entries in feed",feedurl,"..."
		count=0
		session=model.Session()
		entries=session.query(model.Entry.native_id).filter(model.Entry.feed_id==q.id).all()
		#print urls
		for e in E:
		    en=model.Entry(e.id,e.title,e.summary,e.link)
		    if not ((en.native_id,) in entries):#(en.url,) in urls:
			en.feed_id=q.id
			session.add(en)
			print en.url
			print en.title
			print
			count+=1
		session.commit()
		print len(E)-count,"of them are already in db"
    else:
	session=model.Session()
	feeds=session.query(model.Feed).all()
	for q in feeds:
	    if q.lastcheked<time.time()-5:
		print "Feed",q.url,"last modified",time.ctime(q.lastcheked)
		E=feedparser.parse(q.url,modified=time.gmtime(q.lastcheked)).entries
		model.update_feed_time(q)
		print len(E),"new entries in feed",q.url
		entries=session.query(model.Entry.native_id).filter(model.Entry.feed_id==q.id).all()
		#print urls
		for e in E:
		    en=model.Entry(e.id,e.title,e.summary,e.link)
		    if not ((en.native_id,) in entries):
			en.feed_id=q.id
			session.add(en)
			print en.url
			print en.title
			print
		session.commit()
if (__name__=="__main__"):
    main()
