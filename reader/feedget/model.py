# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import ForeignKey,Integer,String,Column,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation,backref
import time


database="/home/avsemenoff/django/diplom0/mydata.db"
engine = create_engine('sqlite:///'+database, module=sqlite)
Base=declarative_base(bind=engine)

class Feed(Base):
    __tablename__='feeds'
    
    id=Column(Integer,primary_key=True)
    url=Column(String)
    last_cheked=Column(Integer)
    
    def __init__(self,url,lastcheked):
	self.url=url
	self.last_cheked=lastcheked
    
    def __repr__(self):
	return "<Feed('%s',%d)>" % (self.url,self.lastcheked)

class Entry(Base):
    __tablename__='entries'
    
    id=Column(Integer,primary_key=True)
    native_id=Column(String)
    title=Column(String)
    summary=Column(String)
    url=Column(String)
 
    feed_id=Column(Integer,ForeignKey('feeds.id'))
    feed=relation(Feed,backref=backref('entries',order_by=id))
 
    def __init__(self,native_id,title,summary,url):
	self.native_id=native_id
	self.title=title
	self.summary=summary
	self.url=url
	
    def __repr__(self):
	return "<Feed('%s','%s','%s','%s')>" % (self.native_id,self.title,self.summary,self.url)

metadata=Base.metadata
metadata.create_all(engine)
Session=sessionmaker()

def add_or_get_feed(feed):
    session=Session()
    f=session.query(Feed).filter(Feed.url==feed.url).first()
    if (not f):
	session.add(feed)
	session.commit()
	return feed
    else:
	return f
	
def de_quot(s):
    return s.replace('"',"&quot;").replace("'","&#039;")

def update_feed_time(feed):
    session=Session()
    session.query(Feed).filter(Feed.url==feed.url).update({Feed.lastcheked:int(time.time())})
    session.commit()
    return session.query(Feed).filter(Feed.url==feed.url).first()